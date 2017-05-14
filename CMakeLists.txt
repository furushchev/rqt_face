cmake_minimum_required(VERSION 2.8.3)
project(rqt_face)

find_package(catkin REQUIRED COMPONENTS
  message_generation
)

catkin_python_setup()

add_message_files(
  FILES
  Emotion.msg
  Gaze.msg
)

generate_messages(DEPENDENCIES)

catkin_package(CATKIN_DEPENDS message_runtime)

install(FILES plugin.xml
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
install(PROGRAMS bin/rqt_face
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

