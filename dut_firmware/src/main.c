#include <zephyr/devicetree.h>
#if defined(CONFIG_CLOCK_CONTROL_NRF)
#include <zephyr/drivers/clock_control.h>
#include <zephyr/drivers/clock_control/nrf_clock_control.h>
#endif /* #if defined(CONFIG_CLOCK_CONTROL_NRF) */
#include <hal/nrf_gpio.h>
#include <zephyr/irq.h>
#include <zephyr/logging/log.h>
#include <nrf.h>
#include <esb.h>
#include <zephyr/kernel.h>
#include <zephyr/types.h>
#include "radio_test.h"

#ifdef CONFIG_SOC_NRF54L15
#include <hal/nrf_oscillators.h>
#include <hal/nrf_clock.h>
#endif

LOG_MODULE_REGISTER(esb_prx, CONFIG_ESB_PRX_APP_LOG_LEVEL);
enum {
	RADIO_TEST_MODE_TX_MOD_CARRIER,
	RADIO_TEST_MODE_TX_UNMOD_CARRIER,
	RADIO_TEST_MODE_RX_MODE,
	RADIO_TEST_MODE_TX_UNMOD_SWEEP,
	RADIO_TEST_MODE_RX_MODE_SWEEP,
	RADIO_TEST_MODE_RANGE_TEST, /* Not implemented */
};



typedef struct __attribute__((packed)) {
	uint8_t first_rf_channel;
	uint8_t last_rf_channel;
	uint8_t radio_power;
	uint8_t datarate;
	uint8_t fem_config;
	uint8_t rf_cmd;

} rf_test_t;
static struct esb_payload rx_payload;
static volatile bool payload_received;

void event_handler(struct esb_evt const *event)
{
	switch (event->evt_id) {
	case ESB_EVENT_TX_SUCCESS:
		LOG_DBG("TX SUCCESS EVENT");
		break;
	case ESB_EVENT_TX_FAILED:
		LOG_DBG("TX FAILED EVENT");
		break;
	case ESB_EVENT_RX_RECEIVED:
		if (esb_read_rx_payload(&rx_payload) == 0) {
			payload_received = true;
		} else {
			LOG_ERR("Error while reading rx packet");
		}
		break;
	}
}

#if defined(CONFIG_CLOCK_CONTROL_NRF)
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
#if defined(NRF54L15_XXAA)
	/* MLTPAN-20 */
	nrf_clock_task_trigger(NRF_CLOCK, NRF_CLOCK_TASK_PLLSTART);
#endif /* defined(NRF54L15_XXAA) */


	LOG_DBG("HF clock started");
	return 0;
}
#endif /* #if defined(CONFIG_CLOCK_CONTROL_NRF) */



	
int esb_initialize(void)
{
	int err;
	/* These are arbitrary default addresses. In end user products
	 * different addresses should be used for each set of devices.
	 */
	uint8_t base_addr_0[4] = { 0x33, 0x44, 0xBB, 0x01 };
	uint8_t base_addr_1[4] = { 0xDE, 0xF0, 0x12, 0x23 };
	uint8_t addr_prefix[8] = { 0x22, 0xBC, 0x66, 0xC4, 0xC5, 0xC6, 0xC7, 0xC8 };

	struct esb_config config = ESB_DEFAULT_CONFIG;

	config.protocol = ESB_PROTOCOL_ESB_DPL;
	config.bitrate = ESB_BITRATE_2MBPS;
	config.mode = ESB_MODE_PRX;
	config.event_handler = event_handler;
	config.selective_auto_ack = true;
	if (IS_ENABLED(CONFIG_ESB_FAST_SWITCHING)) {
		config.use_fast_ramp_up = true;
	}

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

	return 0;
}




int main(void)
{
	int err;
	bool fem = false;
	bool transmitting = false;


	uint8_t pin_pdn = 0xFF;
	uint8_t pin_txen = 0xFF;
	uint8_t pin_rxen = 0xFF;
	uint8_t pin_mode = 0xFF;
	uint8_t pin_antsel = 0xFF;
#ifdef CONFIG_SOC_NRF54L15
	uint32_t load_cap = (volatile uint32_t) NRF_UICR->OTP[0];
	uint32_t fem_config_0 = (volatile uint32_t) NRF_UICR->OTP[1];
	uint32_t fem_config_1 = (volatile uint32_t) NRF_UICR->OTP[2];

	switch(load_cap){
		case 0xFFFFFFFF:
			break;
		case 0:
			nrf_oscillators_hfxo_cap_set(NRF_OSCILLATORS, 0, 0);
			break;
		default:
			nrf_oscillators_hfxo_cap_set(NRF_OSCILLATORS, 1, OSCILLATORS_HFXO_CAP_CALCULATE(NRF_FICR, load_cap/4));}
#else
	uint32_t fem_config_0 = (volatile uint32_t) NRF_UICR->CUSTOMER[1];
	uint32_t fem_config_1 = (volatile uint32_t) NRF_UICR->CUSTOMER[2];
#endif

	if(fem_config_0 != 0xFFFFFFFF || fem_config_1 != 0xFFFFFFFF){
		fem	= true;
		pin_pdn = fem_config_0 & 0xFF;
		pin_txen = (fem_config_0 >> 8) & 0xFF;
		pin_rxen = (fem_config_0 >> 16) & 0xFF;
		pin_mode = (fem_config_0 >> 24) & 0xFF;
		pin_antsel = fem_config_1 & 0xFF;

		if(pin_pdn != 0xFF){
			nrf_gpio_cfg_output(pin_pdn);
			nrf_gpio_pin_write(pin_pdn, 1);
		}
		if(pin_txen != 0xFF){
			nrf_gpio_cfg_output(pin_txen);
			nrf_gpio_pin_write(pin_txen, 0);
		}
		if(pin_rxen != 0xFF){
			nrf_gpio_cfg_output(pin_rxen);
			nrf_gpio_pin_write(pin_rxen, 1);
		}
		if(pin_mode != 0xFF){
			nrf_gpio_cfg_output(pin_mode);
			nrf_gpio_pin_write(pin_mode, 0);
		}
		if(pin_antsel != 0xFF){
			nrf_gpio_cfg_output(pin_antsel);
			nrf_gpio_pin_write(pin_antsel, 0);
		}	
	}

	

#if defined(CONFIG_CLOCK_CONTROL_NRF)
	err = clocks_start();
	if (err) {
		return err;
	}
#endif /* #if defined(CONFIG_CLOCK_CONTROL_NRF) */


	err = esb_initialize();
	if (err) {
		LOG_ERR("ESB initialization failed, err %d", err);
		return err;
	}

	LOG_INF("Initialization complete");
	uint32_t rf_channel = 40;
	esb_set_rf_channel(rf_channel);
	LOG_INF("Setting up for packet receiption on channel %d", rf_channel);

	err = esb_start_rx();
	if (err) {
		LOG_ERR("RX setup failed, err %d", err);
		return err;
	}
	while (1) {
		if (payload_received == true) {
			payload_received = false;
			rf_test_t *rf_test_commands = (rf_test_t *)rx_payload.data;

			LOG_DBG("first_rf_channel: %d", rf_test_commands->first_rf_channel);
			LOG_DBG("last_rf_channel: %d", rf_test_commands->last_rf_channel);
			LOG_DBG("radio_power: %d", rf_test_commands->radio_power);
			LOG_DBG("datarate %d", rf_test_commands->datarate);
			LOG_DBG("fem_config: %d", rf_test_commands->fem_config);
			LOG_DBG("rf_cmd: %d", rf_test_commands->rf_cmd);

			esb_disable();

			static struct radio_test_config my_config;
			memset(&my_config, 0, sizeof(struct radio_test_config));

			switch (rf_test_commands->rf_cmd) {
			case RADIO_TEST_MODE_TX_MOD_CARRIER:
				LOG_INF("RADIO_TEST_MODE_TX_MOD_CARRIER");
				my_config.type = MODULATED_TX;
				my_config.mode = rf_test_commands->datarate;
				my_config.params.modulated_tx.pattern = TRANSMIT_PATTERN_11001100;
				my_config.params.modulated_tx.txpower =
					rf_test_commands->radio_power;
				my_config.params.modulated_tx.channel =
					rf_test_commands->first_rf_channel;
				transmitting = true;
				break;
			case RADIO_TEST_MODE_TX_UNMOD_CARRIER:
				LOG_INF("RADIO_TEST_MODE_TX_UNMOD_CARRIER");
				my_config.type = UNMODULATED_TX;
				my_config.mode = rf_test_commands->datarate;
				my_config.params.unmodulated_tx.txpower =
					rf_test_commands->radio_power;
				my_config.params.unmodulated_tx.channel =
					rf_test_commands->first_rf_channel;
				transmitting = true;
				break;
			case RADIO_TEST_MODE_RX_MODE:
				LOG_INF("RADIO_TEST_MODE_RX_MODE");
				my_config.type = RX;
				my_config.mode = rf_test_commands->datarate;
				my_config.params.rx.channel = rf_test_commands->first_rf_channel;
				break;
			case RADIO_TEST_MODE_TX_UNMOD_SWEEP:
				LOG_INF("RADIO_TEST_MODE_TX_UNMOD_SWEEP");
				my_config.type = TX_SWEEP;
				my_config.mode = rf_test_commands->datarate;
				my_config.params.tx_sweep.txpower = rf_test_commands->radio_power;
				my_config.params.tx_sweep.channel_start =
					rf_test_commands->first_rf_channel;
				my_config.params.tx_sweep.channel_end =
					rf_test_commands->last_rf_channel;
				my_config.params.tx_sweep.delay_ms = 10;
				transmitting = true;
				break;
			case RADIO_TEST_MODE_RX_MODE_SWEEP:
				LOG_INF("RADIO_TEST_MODE_RX_MODE_SWEEP");
				my_config.type = RX_SWEEP;
				my_config.mode = rf_test_commands->datarate;
				my_config.params.rx_sweep.channel_start =
					rf_test_commands->first_rf_channel;
				my_config.params.rx_sweep.channel_end =
					rf_test_commands->last_rf_channel;
				my_config.params.rx_sweep.delay_ms = 10;
				break;
			case RADIO_TEST_MODE_RANGE_TEST:
				LOG_INF("RADIO_TEST_MODE_RANGE_TEST"); /* Not implemented */
				break;
			default:
				LOG_INF("Default case - unsupported command %d",
				       rf_test_commands->rf_cmd);
				break;
			}

			if(fem){
				LOG_INF("FEM config: %d", rf_test_commands->fem_config);
				nrf_gpio_pin_write(pin_mode, rf_test_commands->fem_config & 0x01);
				nrf_gpio_pin_write(pin_antsel, (rf_test_commands->fem_config & 0x02)>>1);
				if(transmitting){
					if(pin_txen != 0xFF){
						nrf_gpio_pin_write(pin_txen, 1);
					}
					if(pin_rxen != 0xFF){
						nrf_gpio_pin_write(pin_rxen, 0);
					}
				}
			}

		
			radio_test_init(&my_config);
			/* Start radio test - needs a physical reset to stop or retest */
			radio_test_start(&my_config);
			return 0;
		}
		k_msleep(100);
	}
	/* return to idle thread */
	return 0;
}
