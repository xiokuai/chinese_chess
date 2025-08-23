cmake_minimum_required(VERSION 3.10)
project(alpha_beta_search)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_library(alpha_beta_search SHARED alpha_beta_search.cpp zobrist_hasher.cpp)

target_compile_options(alpha_beta_search PRIVATE -O2)

if (APPLE)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fexperimental-library")
endif()

if(WIN32)
    set_target_properties(alpha_beta_search PROPERTIES SUFFIX ".dll")
elseif(APPLE)
    set_target_properties(alpha_beta_search PROPERTIES SUFFIX ".dylib")
else()
    set_target_properties(alpha_beta_search PROPERTIES SUFFIX ".so")
endif()
