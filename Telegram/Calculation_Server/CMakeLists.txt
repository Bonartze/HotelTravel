cmake_minimum_required(VERSION 3.10)

project(CalculationServer)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)
include_directories(${CMAKE_SOURCE_DIR}/../../third_party/json/include)
include_directories(${CMAKE_SOURCE_DIR}/third_party/json/include)
find_package(Boost 1.70 REQUIRED COMPONENTS system)

if (Boost_FOUND)
    include_directories(${Boost_INCLUDE_DIRS})
else ()
    message(FATAL_ERROR "Could not find Boost!")
endif ()

add_executable(CalculationServer Server.cpp Calculations.cpp)

target_link_libraries(CalculationServer ${Boost_LIBRARIES})
