add_compile_options(-Wall -Wextra -Wpedantic)
add_compile_options(-Werror)
add_compile_options(-Wmissing-prototypes -Wredundant-decls -Wshadow -Wpointer-arith)
add_compile_options(-O3 -fwrapv)

set(UTILS_SRC utils.c)
add_library(utils STATIC ${UTILS_SRC})

set(AES256GCM_SRC aes256gcm.c)
add_library(aes256gcm STATIC ${AES256GCM_SRC})
target_link_libraries(aes256gcm PUBLIC ${OPENSSL_CRYPTO_LIBRARY})

set(GCWR_AKE_SRC gcwr-ake.c)
add_library(gcwr-ake STATIC ${GCWR_AKE_SRC})
target_link_libraries(gcwr-ake oqs ${OPENSSL_CRYPTO_LIBRARY} utils)
