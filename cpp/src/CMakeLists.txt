add_executable(main main.cpp)

find_package(OpenCV REQUIRED)
if (OpenCV_FOUND)
    target_include_directories(main PUBLIC ${OpenCV_INCLUDE_DIRS})
    target_link_libraries(main ${OpenCV_LIBS})
endif()