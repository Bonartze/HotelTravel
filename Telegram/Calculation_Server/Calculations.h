#ifndef CALCULATIONSERVER_CALCULATIONS_H
#define CALCULATIONSERVER_CALCULATIONS_H

#include <iostream>
#include <any>
#include <string>
#include <nlohmann/json.hpp>
#include <fstream>
#include <cmath>


class Calculations {
private:
    nlohmann::json json_data;
public:
    Calculations();

    std::any get_answer(const std::string &);

    double calculate_median();

    double calculate_average_hotel_price();

    double calculate_average_rating();

    double calculate_correlation_price_rating();

    double calculate_std_deviation();
};


#endif //CALCULATIONSERVER_CALCULATIONS_H
