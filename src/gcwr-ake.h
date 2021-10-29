#include <stdio.h>
#include <string.h>
#include <oqs/oqs.h>

#include "utils.h"

#define MAX 16

void concat_keys(const uint8_t *key1, const uint8_t *key2, const uint8_t *key3,
                 size_t length, uint8_t *out);

void ake_init(OQS_KEM* kem,
              uint8_t* dkA1,
              uint8_t* ekB1,
              uint8_t* cA1,
              uint8_t* kA1,
              uint8_t* ekA2,
              uint8_t* dkA2);

void ake_algA(OQS_KEM* kem,
              const uint8_t* ekA1,
              const uint8_t* ekA2,
              const uint8_t* dkB1,
              uint8_t* kB1,
              uint8_t* kB2,
              uint8_t* cA1,
              uint8_t* cB1,
              uint8_t* cB2,
              uint8_t* kA1,
              uint8_t* skB);

void ake_algB(OQS_KEM* kem,
              const uint8_t* cB1,
              const uint8_t* cB2,
              const uint8_t* dkA1,
              const uint8_t* dkA2,
              const uint8_t* kA1,
              uint8_t* sk);
