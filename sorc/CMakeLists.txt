if(BUILD_GFS_UTILS)
	add_custom_command(
		OUTPUT "${PROJECT_BINARY_DIR}/gaussian_sfcanl.x"
		COMMAND "BUILD_TYPE=${CMAKE_BUILD_TYPE} ush/build.sh"
		WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/gfs_utils.fd
		)
endif()
