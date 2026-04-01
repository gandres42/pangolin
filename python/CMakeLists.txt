include_directories( ${PROJECT_SOURCE_DIR}/include)
include_directories( "/usr/include/eigen3" )

if(POLICY CMP0057)
	cmake_policy(SET CMP0057 NEW)
endif()

# Prefer a modern pybind11 package (needed for newer Python versions).
find_package(Python3 COMPONENTS Interpreter Development.Module QUIET)
if(Python3_Interpreter_FOUND)
	execute_process(
		COMMAND "${Python3_EXECUTABLE}" -m pybind11 --cmakedir
		RESULT_VARIABLE PYBIND11_CMAKEDIR_RESULT
		OUTPUT_VARIABLE PYBIND11_CMAKEDIR
		OUTPUT_STRIP_TRAILING_WHITESPACE
		ERROR_QUIET
	)
	if(PYBIND11_CMAKEDIR_RESULT EQUAL 0 AND PYBIND11_CMAKEDIR)
		list(APPEND CMAKE_PREFIX_PATH "${PYBIND11_CMAKEDIR}")
	endif()
endif()

set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 CONFIG QUIET)
if(NOT pybind11_FOUND)
	# Fallback to vendored legacy pybind11 if no external package is available.
	LIST(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/external/pybind11/tools)
	include_directories(${PROJECT_SOURCE_DIR}/external/pybind11/include)
	include(pybind11Tools)
endif()


pybind11_add_module( pangolin pangolin.cpp )
SET_TARGET_PROPERTIES(pangolin PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR})
target_link_libraries( pangolin PRIVATE ${LIBRARY_NAME})