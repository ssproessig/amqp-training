cmake_minimum_required(VERSION 3.11)
project(amqp LANGUAGES CXX)

include(Qt_and_C++_settings.cmake)

add_subdirectory(lib)

add_executable(consumer src/consumer.cpp)
target_link_libraries(consumer qamqp-lib Qt5::Core Qt5::Network)
