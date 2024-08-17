#include "Calculations.h"

using json = nlohmann::json;

Calculations::Calculations() {
    json_data = json::parse(std::ifstream("../../../JsonData/hotels_data.json"));
}

std::any Calculations::get_answer(const std::string &message) {

    if (message == "median\n")
        return calculate_median();
    else if (message == "std_deviation\n")
        return calculate_std_deviation();
    else if (message == "average_hotel_price\n")
        return calculate_average_hotel_price();
    else if (message == "average_rating\n")
        return calculate_average_rating();
    else if (message == "correlation_price_rating\n")
        return calculate_correlation_price_rating();
    return "None\n";
}

double Calculations::calculate_median() {
    std::vector<double> prices;

    for (auto &i: json_data) {
        if (i.contains("price")) {
            std::string price_str = i["price"].get<std::string>();

            price_str.erase(std::remove(price_str.begin(), price_str.end(), '$'), price_str.end());

            try {
                double price = std::stod(price_str);
                prices.push_back(price);
            } catch (const std::invalid_argument &e) {
                std::cerr << "Invalid price format: " << price_str << std::endl;
            }
        }
    }

    if (prices.empty()) {
        std::cerr << "No valid prices found." << std::endl;
        return 0.0;
    }

    std::sort(prices.begin(), prices.end());

    size_t n = prices.size();
    double median;

    if (n % 2 == 0) {
        median = (prices[n / 2 - 1] + prices[n / 2]) / 2.0;
    } else {
        median = prices[n / 2];
    }

    return median;
}

double Calculations::calculate_average_hotel_price() {
    double total_price = 0.0;
    int count = 0;

    for (auto &i: json_data) {
        if (i.contains("price")) {
            std::string price_str = i["price"].get<std::string>();

            price_str.erase(std::remove(price_str.begin(), price_str.end(), '$'), price_str.end());

            double price = std::stod(price_str);

            total_price += price;
            count++;
        }
    }

    double average_price = (count > 0) ? total_price / count : 0.0;
    return average_price;
}

double Calculations::calculate_average_rating() {
    double total_rate = 0.0;
    int count = 0;

    for (auto &i: json_data) {
        if (i.contains("hotel_evaluation")) {
            std::string price_str = i["hotel_evaluation"].get<std::string>();
            price_str = price_str.substr(7);
            double price = std::stod(price_str);

            total_rate += price;
            count++;
        }
        double average_rate = (count > 0) ? total_rate / count : 0.0;
        return average_rate;
    }
    return 0;
}

double Calculations::calculate_correlation_price_rating() {
    std::vector<double> prices;
    std::vector<double> ratings;

    for (auto &i: json_data) {
        if (i.contains("price") && i.contains("hotel_evaluation")) {
            std::string price_str = i["price"].get<std::string>();
            std::string rating_str = i["hotel_evaluation"].get<std::string>();
            price_str.erase(std::remove(price_str.begin(), price_str.end(), '$'), price_str.end());
            rating_str = rating_str.substr(7);
            try {
                double price = std::stod(price_str);
                double rating = std::stod(rating_str);

                prices.push_back(price);
                ratings.push_back(rating);
            } catch (const std::invalid_argument &e) {
                std::cerr << "Invalid price or rating format: " << price_str << ", " << rating_str << std::endl;
            }
        }
    }

    if (prices.size() != ratings.size() || prices.size() < 2) {
        std::cerr << "Not enough valid data to calculate correlation." << std::endl;
        return 0.0;
    }

    double mean_price = std::accumulate(prices.begin(), prices.end(), 0.0) / prices.size();
    double mean_rating = std::accumulate(ratings.begin(), ratings.end(), 0.0) / ratings.size();

    double covariance = 0.0;
    double variance_price = 0.0;
    double variance_rating = 0.0;

    for (size_t i = 0; i < prices.size(); ++i) {
        double price_diff = prices[i] - mean_price;
        double rating_diff = ratings[i] - mean_rating;

        covariance += price_diff * rating_diff;
        variance_price += price_diff * price_diff;
        variance_rating += rating_diff * rating_diff;
    }

    double correlation = covariance / std::sqrt(variance_price * variance_rating);

    return correlation;

}

double Calculations::calculate_std_deviation() {
    std::vector<double> prices;

    for (auto &i: json_data) {
        if (i.contains("price")) {
            std::string price_str = i["price"].get<std::string>();

            price_str.erase(std::remove(price_str.begin(), price_str.end(), '$'), price_str.end());

            try {
                double price = std::stod(price_str);
                prices.push_back(price);
            } catch (const std::invalid_argument &e) {
                std::cerr << "Invalid price format: " << price_str << std::endl;
            }
        }
    }

    if (prices.empty()) {
        std::cerr << "Not enough valid data to calculate standard deviation." << std::endl;
        return 0.0;
    }

    double mean = std::accumulate(prices.begin(), prices.end(), 0.0) / prices.size();

    double variance_sum = 0.0;
    for (const double &price: prices) {
        variance_sum += std::pow(price - mean, 2);
    }

    double variance = variance_sum / prices.size();

    double standard_deviation = std::sqrt(variance);

    return standard_deviation;
}