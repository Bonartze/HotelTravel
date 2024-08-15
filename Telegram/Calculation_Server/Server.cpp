#include <boost/asio.hpp>
#include <iostream>
#include <thread>
#include "Server.h"

void handle_client(boost::asio::ip::tcp::socket socket) {
    try {
        Calculations calc;
        boost::asio::streambuf buffer;
        boost::system::error_code error;

        boost::asio::read_until(socket, buffer, '\n', error);
        if (error) {
            std::cerr << "Error reading data: " << error.message() << std::endl;
            return;
        }

        std::string message = boost::asio::buffer_cast<const char *>(buffer.data());
        std::any resp = calc.get_answer(message);
        std::string response;
        if (resp.type() == typeid(std::string))
            response = std::any_cast<std::string>(resp);
        else if (resp.type() == typeid(double))
            response = std::to_string(std::any_cast<double>(resp));

        boost::asio::write(socket, boost::asio::buffer(response), error);
        if (error) {
            std::cerr << "Error writing data: " << error.message() << std::endl;
        }
    } catch (const std::exception &e) {
        std::cerr << "Exception in thread: " << e.what() << std::endl;
    }
}

int main() {
    try {
        boost::asio::io_context io_context;
        boost::asio::ip::tcp::acceptor acceptor(io_context,
                                                boost::asio::ip::tcp::endpoint(boost::asio::ip::tcp::v4(), 8888));

        std::cout << "TCP Echo Server started. Listening on port 8888." << std::endl;

        while (true) {
            boost::asio::ip::tcp::socket socket(io_context);
            acceptor.accept(socket);

            std::cout << "New connection from: " << socket.remote_endpoint() << std::endl;

            std::thread(handle_client, std::move(socket)).detach();
        }
    } catch (const std::exception &e) {
        std::cerr << "Exception in main: " << e.what() << std::endl;
    }

    return 0;
}
