add_compile_options(-Wall -Wextra -Wpedantic)
add_compile_options(-Werror)
add_compile_options(-Wmissing-prototypes -Wredundant-decls -Wshadow -Wpointer-arith)
add_compile_options(-O3 -fwrapv)

add_executable(test_aes256gcm ../src/utils.c test_aes256gcm.c)
target_link_libraries(test_aes256gcm PUBLIC aes256gcm)

set(TEST_GCWR_AKE_SRCS ../src/gcwr-ake.c test-gcwr-ake.c)
add_executable(test_gcwr_ake ${TEST_GCWR_AKE_SRCS})
target_link_libraries(test_gcwr_ake PUBLIC utils gcwr-ake)

set(TEST_INDCCA ../src/indcca.c test_indcca.c)
add_executable(test_indcca ${TEST_INDCCA})
target_link_libraries(test_indcca PUBLIC oqs utils indcca aes256gcm)

add_test(NAME aes256gcm COMMAND test_aes256gcm)
add_test(NAME test_gcwr_ake COMMAND test_gcwr_ake)
add_test(NAME test_indcca COMMAND test_indcca)
