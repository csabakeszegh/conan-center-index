cmake_minimum_required(VERSION 3.25)

file(READ src/ZeDMD.h version)
string(REGEX MATCH "ZEDMD_VERSION_MAJOR[ ]+([0-9]+)" _tmp ${version})
set(VERSION_MAJOR "${CMAKE_MATCH_1}")
string(REGEX MATCH "ZEDMD_VERSION_MINOR[ ]+([0-9]+)" _tmp ${version})
set(VERSION_MINOR "${CMAKE_MATCH_1}")
string(REGEX MATCH "ZEDMD_VERSION_PATCH[ ]+([0-9]+)" _tmp ${version})
set(VERSION_PATCH "${CMAKE_MATCH_1}")

project(zedmd VERSION "${VERSION_MAJOR}.${VERSION_MINOR}.${VERSION_PATCH}"
   DESCRIPTION "Cross-platform library for communicating with ZeDMD." LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_C_STANDARD 99)

set(CMAKE_CXX_VISIBILITY_PRESET hidden)
set(CMAKE_C_VISIBILITY_PRESET hidden)

add_library(zedmd
    src/ZeDMDComm.h
    src/ZeDMDComm.cpp
    src/ZeDMDWiFi.h
    src/ZeDMDWiFi.cpp
    src/ZeDMD.h
    src/ZeDMD.cpp
)
add_library(zedmd::zedmd ALIAS zedmd)

find_package(miniz REQUIRED)
find_package(libframeutil REQUIRED)
find_package(komihash REQUIRED)
find_package(sockpp REQUIRED)
find_package(libserialport REQUIRED)
find_package(Threads REQUIRED)

target_link_libraries(zedmd PRIVATE
    miniz::miniz
    sockpp::sockpp
    komihash::komihash
    libframeutil::libframeutil
    libserialport::libserialport
    Threads::Threads
)


find_package(cargs REQUIRED)
add_executable(zedmd-client 
    src/client.cpp
)
target_link_libraries(zedmd-client PRIVATE
    zedmd::zedmd
    cargs::cargs
    libserialport::libserialport
)

install(TARGETS zedmd DESTINATION lib)
install(FILES src/ZeDMDComm.h src/ZeDMDWiFi.h src/ZeDMD.h DESTINATION include)
install(TARGETS zedmd-client DESTINATION bin)