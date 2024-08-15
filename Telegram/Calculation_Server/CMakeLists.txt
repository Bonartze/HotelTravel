cmake_minimum_required(VERSION 3.10)

# Set the project name
project(CalculationServer)

# Set the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)
include_directories(${CMAKE_SOURCE_DIR}/../../third_party/json/include)
# Find Boost
find_package(Boost 1.70 REQUIRED COMPONENTS system)

if (Boost_FOUND)
    include_directories(${Boost_INCLUDE_DIRS})
else ()
    message(FATAL_ERROR "Could not find Boost!")
endif ()

# Add the executable
add_executable(CalculationServer Server.cpp Calculations.cpp)

# Link Boost libraries
target_link_libraries(CalculationServer ${Boost_LIBRARIES})
