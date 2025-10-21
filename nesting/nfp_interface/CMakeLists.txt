cmake_minimum_required(VERSION 3.12)
project(libnfporb_interface)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)  # ensures -fPIC automatically

# Find Python properly
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

# Include Boost if needed
if(DEFINED ENV{BOOST_ROOT})
    include_directories($ENV{BOOST_ROOT})
endif()

# Include Python headers
include_directories(${Python3_INCLUDE_DIRS})

# Build shared library
add_library(${PROJECT_NAME} SHARED libnfporb_interface.cpp)

# Link against Python
target_link_libraries(${PROJECT_NAME} PRIVATE ${Python3_LIBRARIES})
