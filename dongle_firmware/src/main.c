#include <zephyr/kernel.h>
#include <zephyr/init.h>
#include <zephyr/sys/byteorder.h>
#include <zephyr/usb/usb_device.h>
#include <zephyr/drivers/clock_control.h>
#include <zephyr/drivers/clock_control/nrf_clock_control.h>
#include <esb.h>

#define LOG_LEVEL LOG_LEVEL_DBG
LOG_MODULE_REGISTER(main);

#define RF_TEST_VERSION 0x010000

#define LOOPBACK_OUT_EP_ADDR 0x01
#define LOOPBACK_IN_EP_ADDR 0x81
#define LOOPBACK_BULK_EP_MPS 64
#define LOOPBACK_OUT_EP_IDX 0
#define LOOPBACK_IN_EP_IDX 2

/* USB command defines */
#define CMD_FIRMWARE_VERSION 1
#define CMD_INIT_RF 10
#define CMD_SEND_PACKET 11
#define CMD_STATUS_PACKET 12

static uint8_t loopback_buf[LOOPBACK_BULK_EP_MPS];
static volatile bool rf_sent_successfully = false;
static struct esb_payload rf_payload;

struct usb_loopback_config {
	struct usb_if_descriptor if0;
	struct usb_ep_descriptor if0_out_ep;
	struct usb_ep_descriptor if0_in_ep;
	struct usb_ep_descriptor test;
} __packed;

typedef struct __attribute__((packed)) {
	uint8_t first_rf_channel;
	uint8_t last_rf_channel;
	uint8_t radio_power;
	uint8_t datarate;
	uint8_t fem_config;
	uint8_t rf_cmd;
	uint8_t usb_cmd;
} rf_test_t;

USBD_CLASS_DESCR_DEFINE(primary, 0) struct usb_loopback_config loopback_cfg = {
	/* Interface descriptor 0 */
	.if0 = {
		.bLength = sizeof(struct usb_if_descriptor),
		.bDescriptorType = USB_DESC_INTERFACE,
		.bInterfaceNumber = 0,
		.bAlternateSetting = 0,
		.bNumEndpoints = 3,
		.bInterfaceClass = USB_BCC_VENDOR,
		.bInterfaceSubClass = USB_BCC_VENDOR,
		.bInterfaceProtocol = 0xff,
		.iInterface = 0,
	},

	/* Data Endpoint OUT */
	.if0_out_ep = {
		.bLength = sizeof(struct usb_ep_descriptor),
		.bDescriptorType = USB_DESC_ENDPOINT,
		.bEndpointAddress = LOOPBACK_OUT_EP_ADDR,
		.bmAttributes = USB_DC_EP_BULK,
		.wMaxPacketSize = sys_cpu_to_le16(LOOPBACK_BULK_EP_MPS),
		.bInterval = 0x06,
	},

	/* Data Endpoint IN */
	.if0_in_ep = {
		.bLength = sizeof(struct usb_ep_descriptor),
		.bDescriptorType = USB_DESC_ENDPOINT,
		.bEndpointAddress = LOOPBACK_IN_EP_ADDR,
		.bmAttributes = USB_DC_EP_BULK,
		.wMaxPacketSize = sys_cpu_to_le16(LOOPBACK_BULK_EP_MPS),
		.bInterval = 0x06,
	},
	/* Data Endpoint IN */
	.test= {
		.bLength = sizeof(struct usb_ep_descriptor),
		.bDescriptorType = USB_DESC_ENDPOINT,
		.bEndpointAddress = LOOPBACK_IN_EP_ADDR,
		.bmAttributes = USB_DC_EP_BULK,
		.wMaxPacketSize = sys_cpu_to_le16(LOOPBACK_BULK_EP_MPS),
		.bInterval = 0x06,
	},
};
/* usb.rst vendor handler end */

void parse_commands(uint8_t ep, uint8_t *usb_out_data, int length);

static void loopback_interface_config(struct usb_desc_header *head, uint8_t bInterfaceNumber)
{
	ARG_UNUSED(head);

	loopback_cfg.if0.bInterfaceNumber = bInterfaceNumber;
}

/* usb.rst vendor handler start */
static int loopback_vendor_handler(struct usb_setup_packet *setup, int32_t *len, uint8_t **data)
{
	LOG_DBG("Class request: bRequest 0x%x bmRequestType 0x%x len %d", setup->bRequest,
		setup->bmRequestType, *len);

	if (setup->RequestType.recipient != USB_REQTYPE_RECIPIENT_DEVICE) {
		return -ENOTSUP;
	}

	if (usb_reqtype_is_to_device(setup) && setup->bRequest == 0x5b) {
		LOG_DBG("Host-to-Device, data %p", *data);
		/*
		 * Copy request data in loopback_buf buffer and reuse
		 * it later in control device-to-host transfer.
		 */
		memcpy(loopback_buf, *data, MIN(sizeof(loopback_buf), setup->wLength));
		return 0;
	}

	if ((usb_reqtype_is_to_host(setup)) && (setup->bRequest == 0x5c)) {
		LOG_DBG("Device-to-Host, wLength %d, data %p", setup->wLength, *data);
		*data = loopback_buf;
		*len = MIN(sizeof(loopback_buf), setup->wLength);
		return 0;
	}

	return -ENOTSUP;
}

static void loopback_out_cb(uint8_t ep, enum usb_dc_ep_cb_status_code ep_status)
{
	uint32_t bytes_to_read;

	usb_read(ep, NULL, 0, &bytes_to_read);
	LOG_DBG("ep 0x%x, bytes to read %d ", ep, bytes_to_read);
	usb_read(ep, loopback_buf, bytes_to_read, NULL);
	for (int i = 0; i < bytes_to_read; i++)
		LOG_DBG("%x", loopback_buf[i]);
	parse_commands(ep, loopback_buf, bytes_to_read);
}

static void loopback_in_cb(uint8_t ep, enum usb_dc_ep_cb_status_code ep_status)
{
}

static struct usb_ep_cfg_data ep_cfg[] = {
	{
		.ep_cb = loopback_out_cb,
		.ep_addr = LOOPBACK_OUT_EP_ADDR,
	},
	{
		.ep_cb = loopback_in_cb,
		.ep_addr = LOOPBACK_IN_EP_ADDR,
	},
};

static void loopback_status_cb(struct usb_cfg_data *cfg, enum usb_dc_status_code status,
			       const uint8_t *param)
{
	ARG_UNUSED(cfg);

	switch (status) {
	case USB_DC_CONFIGURED:
		LOG_DBG("USB configured");
		break;
	case USB_DC_INTERFACE:
		LOG_DBG("USB interface configured");
		break;
	case USB_DC_SET_HALT:
		LOG_DBG("Set Feature ENDPOINT_HALT");
		break;
	case USB_DC_CLEAR_HALT:
		LOG_DBG("Clear Feature ENDPOINT_HALT");
		break;
	case USB_DC_SOF:
		/* Just ignore */
		break;
	default:
		LOG_DBG("Unhandled status cb: %d", status);
		break;
	}
}

USBD_DEFINE_CFG_DATA(loopback_config) = {
	.usb_device_description = NULL,
	.interface_config = loopback_interface_config,
	.interface_descriptor = &loopback_cfg.if0,
	.cb_usb_status = loopback_status_cb,
	.interface = {
		.class_handler = NULL,
		.custom_handler = NULL,
		.vendor_handler = loopback_vendor_handler,
	},
	.num_endpoints = ARRAY_SIZE(ep_cfg),
	.endpoint = ep_cfg,
};

void parse_commands(uint8_t ep, uint8_t *usb_out_data, int length)
{
	if (usb_out_data == NULL || length > sizeof(rf_test_t)) {
		LOG_ERR("NULL ptr or Length mismatch %x", length);
		return;
	}

	rf_test_t *rf_test_command = (rf_test_t *)usb_out_data;
	LOG_DBG("USB command %x", rf_test_command->usb_cmd);
	switch (rf_test_command->usb_cmd) {
	case CMD_FIRMWARE_VERSION: {
		uint32_t version = sys_be32_to_cpu(RF_TEST_VERSION);
		LOG_INF("FIRMWARE_VERISON: %d",version);
		usb_write(0x82, (uint8_t *)&version, sizeof(version), NULL);
	} break;

	case CMD_SEND_PACKET:
		rf_payload.length = 6;
		memcpy(rf_payload.data, rf_test_command, rf_payload.length);
		LOG_DBG("rf_payload: %d", rf_payload.data);
		if (esb_write_payload(&rf_payload)) {
			LOG_ERR("Failed to send payload");
		}
		break;

	case CMD_STATUS_PACKET:
			static uint8_t temp_usb_byte;
			temp_usb_byte = rf_sent_successfully;

			int ret = usb_write(0x82, &temp_usb_byte, 1, NULL);
			if (ret) {
				LOG_ERR("usb rf ack write error %d", ret);
			}
		if (rf_sent_successfully) {
			rf_sent_successfully = false;
		}
		break;

	default:
		/* Many events will end up here, as there's no need to add RF test support locally to this device */
		break;
	}
}

void event_handler(struct esb_evt const *event)
{
	switch (event->evt_id) {
	case ESB_EVENT_TX_SUCCESS:
		rf_sent_successfully = true;
		LOG_DBG("TX SUCCESS EVENT");
		break;
	case ESB_EVENT_TX_FAILED:
		LOG_DBG("TX FAILED EVENT");
		break;
	case ESB_EVENT_RX_RECEIVED:
		LOG_INF("Packet received");
		if (esb_read_rx_payload(&rf_payload) == 0) {
		} else {
			LOG_ERR("Error while reading rx packet");
		}
		break;
	}
}

int esb_initialize(void)
{
	int err;
	uint8_t base_addr_0[4] = { 0x33, 0x44, 0xBB, 0x01 };
	uint8_t base_addr_1[4] = { 0xDE, 0xF0, 0x12, 0x23 };
	uint8_t addr_prefix[8] = { 0x22, 0xBC, 0x66, 0xC4, 0xC5, 0xC6, 0xC7, 0xC8 };


	struct esb_config config = ESB_DEFAULT_CONFIG;

	config.protocol = ESB_PROTOCOL_ESB_DPL;
	config.bitrate = ESB_BITRATE_2MBPS;
	config.mode = ESB_MODE_PTX;
	config.event_handler = event_handler;
	config.selective_auto_ack = true;

	err = esb_init(&config);
	if (err) {
		return err;
	}

	err = esb_set_base_address_0(base_addr_0);
	if (err) {
		return err;
	}

	err = esb_set_base_address_1(base_addr_1);
	if (err) {
		return err;
	}

	err = esb_set_prefixes(addr_prefix, ARRAY_SIZE(addr_prefix));
	if (err) {
		return err;
	}

	err = esb_set_rf_channel(40);
	if (err) {
		return err;
	}

	return 0;
}

int clocks_start(void)
{
	int err;
	int res;
	struct onoff_manager *clk_mgr;
	struct onoff_client clk_cli;

	clk_mgr = z_nrf_clock_control_get_onoff(CLOCK_CONTROL_NRF_SUBSYS_HF);
	if (!clk_mgr) {
		LOG_ERR("Unable to get the Clock manager");
		return -ENXIO;
	}

	sys_notify_init_spinwait(&clk_cli.notify);

	err = onoff_request(clk_mgr, &clk_cli);
	if (err < 0) {
		LOG_ERR("Clock request failed: %d", err);
		return err;
	}

	do {
		err = sys_notify_fetch_result(&clk_cli.notify, &res);
		if (!err && res) {
			LOG_ERR("Clock could not be started: %d", res);
			return res;
		}
	} while (err);

	LOG_DBG("HF clock started");
	return 0;
}

int main(void)
{
	int ret = clocks_start();
	if (ret) {
		LOG_ERR("Clock init failed %d", ret);
		return ret;
	}
	ret = usb_enable(NULL);
	if (ret) {
		LOG_ERR("USB enable failed %d", ret);
		return ret;
	}
	ret = esb_initialize();
	if (ret) {
		LOG_ERR("ESB init failed %d", ret);
		return ret;
	}
	return 0;
}
