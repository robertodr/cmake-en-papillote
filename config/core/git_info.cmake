
# Copyright (c) 2015 by Radovan Bast and Jonas Juselius
# see https://github.com/cmake-en-papillote/cmake-en-papillote/blob/master/LICENSE

#-------------------------------------------------------------------------------

function(get_git_info
         in_python_executable
         out_git_last_commit_hash
         out_git_last_commit_author
         out_git_last_commit_date
         out_git_branch
         out_git_status_at_build)

    find_package(Git)
    if(GIT_FOUND)
        execute_process(
            COMMAND ${GIT_EXECUTABLE} rev-list --max-count=1 --abbrev-commit HEAD
            OUTPUT_VARIABLE _git_last_commit_hash
            ERROR_QUIET
            )

        if(_git_last_commit_hash)
            string(STRIP ${_git_last_commit_hash} _git_last_commit_hash)
        endif()

        execute_process(
            COMMAND ${GIT_EXECUTABLE} log --max-count=1 HEAD
            OUTPUT_VARIABLE _git_last_commit
            ERROR_QUIET
            )

        if(_git_last_commit)
            string(REGEX MATCH "Author:[ ]*(.+)<" temp "${_git_last_commit}")
            set(_git_last_commit_author ${CMAKE_MATCH_1})
            string(REGEX MATCH "Date:[ ]*(.+(\\+|-)[0-9][0-9][0-9][0-9])" temp "${_git_last_commit}")
            set(_git_last_commit_date ${CMAKE_MATCH_1})
        endif()

        execute_process(
            COMMAND ${in_python_executable} -c "import subprocess; import re; print(re.search(r'\\*.*', subprocess.Popen(['${GIT_EXECUTABLE}', 'branch'], stdout=subprocess.PIPE).communicate()[0], re.MULTILINE).group())"
            OUTPUT_VARIABLE _git_branch
            ERROR_QUIET
            )

        if(_git_branch)
            string(REPLACE "*" "" _git_branch ${_git_branch})
            string(STRIP ${_git_branch} _git_branch)
        endif()

        execute_process(
            COMMAND ${GIT_EXECUTABLE} status -uno
            OUTPUT_VARIABLE _git_status_at_build
            ERROR_QUIET
        )

        set(${out_git_last_commit_hash}   ${_git_last_commit_hash}   PARENT_SCOPE)
        set(${out_git_last_commit_author} ${_git_last_commit_author} PARENT_SCOPE)
        set(${out_git_last_commit_date}   ${_git_last_commit_date}   PARENT_SCOPE)
        set(${out_git_branch}             ${_git_branch}             PARENT_SCOPE)
        set(${out_git_status_at_build}    ${_git_status_at_build}    PARENT_SCOPE)
    else()
        set(${out_git_last_commit_hash}   "" PARENT_SCOPE)
        set(${out_git_last_commit_author} "" PARENT_SCOPE)
        set(${out_git_last_commit_date}   "" PARENT_SCOPE)
        set(${out_git_branch}             "" PARENT_SCOPE)
        set(${out_git_status_at_build}    "" PARENT_SCOPE)
    endif()
endfunction()
