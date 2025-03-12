#
# Copyright (c) 2018 Nordic Semiconductor
#
# SPDX-License-Identifier: LicenseRef-Nordic-5-Clause
#
cmake_minimum_required(VERSION 3.20.0)

find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(NONE)

zephyr_include_directories(src)
FILE(GLOB app_sources src/*.c)
target_sources(app PRIVATE ${app_sources})
set(SB_CONF_FILE sysbuild.conf)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
