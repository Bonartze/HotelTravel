#ifndef HOTTELTRAVEL_SEVER_H
#define HOTTELTRAVEL_SEVER_H

#pragma once

#include <boost/asio.hpp>
#include "Calculations.h"

void handle_client(boost::asio::ip::tcp::socket);

#endif //HOTTELTRAVEL_SEVER_H