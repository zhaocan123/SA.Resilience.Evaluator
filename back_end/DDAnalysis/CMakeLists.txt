# CMakeList.txt: SecurityVulnerability 的 CMake 项目，在此处包括源代码并定义
# 项目特定的逻辑。
#
cmake_minimum_required (VERSION 3.8)
project ("DDAnalysis")



# TODO: 如有需要，请添加测试并安装目标。
set(LLVM_DIR "/temp_redis/llvm-project-llvmorg-15.0.2-new/build/lib/cmake/llvm")
find_package(LLVM REQUIRED CONFIG)
set(Clang_DIR "/temp_redis/llvm-project-llvmorg-15.0.2-new/build/lib/cmake/clang")
find_package(Clang REQUIRED CONFIG)

include_directories("/temp_redis/llvm-project-llvmorg-15.0.2-new/clang/include")
include_directories("/temp_redis/llvm-project-llvmorg-15.0.2-new/llvm/include")
include_directories("/temp_redis/llvm-project-llvmorg-15.0.2-new/build/include")
include_directories("/temp_redis/llvm-project-llvmorg-15.0.2-new/build/tools/clang/include")

set(AUTESTSRC
DDAnalysis.cpp
)

set(CLANG_LINK_LIBRARIES
libclang
clangTooling
clangARCMigrate
clangAST
clangASTMatchers
clangAnalysis
clangBasic
clangCodeGen
clangDriver
clangEdit
clangFrontend
clangFrontendTool
clangLex
clangParse
clangRewrite
clangRewriteFrontend
clangSema
clangSerialization
clangCodeGen
)

function(clang_target_link target type)
if (CLANG_LINK_CLANG_DYLIB)
    target_link_libraries(${target} ${type} clang_shared)
else()
    target_link_libraries(${target} ${type} ${ARGN})
endif()
endfunction()

add_executable(${PROJECT_NAME} ${HEAD_FILES} ${AUTESTSRC})

clang_target_link(${PROJECT_NAME} PRIVATE ${CLANG_LINK_LIBRARIES})


