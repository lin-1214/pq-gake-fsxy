#include <stdio.h>
#include <string.h>
#include <oqs/oqs.h>
#include <time.h>
#include <sys/times.h>
#include <unistd.h>

#define MAX 16

void print_stats(clock_t begin_init,
                 clock_t end_init,
                 clock_t end_keys,
                 clock_t end_alg_init,
                 clock_t end_algB,
                 clock_t end_algA,
                 clock_t end_total) {

   int CLOCK_TICKS = sysconf(_SC_CLK_TCK);
   double time_init     = (double)(end_init - begin_init) / CLOCK_TICKS;
   double time_keys     = (double)(end_keys - end_init) / CLOCK_TICKS;
   double time_alg_init = (double)(end_alg_init - end_keys) / CLOCK_TICKS;
   double time_alg_b    = (double)(end_algB - end_alg_init) / CLOCK_TICKS;
   double time_alg_a    = (double)(end_algA - end_algB) / CLOCK_TICKS;
   double time_total    = (double)(end_total - end_init) / CLOCK_TICKS;

   printf("\n\nTime stats\n");
   printf("\tInit time       : %.3fs (%.2f%%)\n", time_init, time_init*100/time_total);
   printf("\tRound keys time : %.3fs (%.2f%%)\n", time_keys, time_keys*100/time_total);
   printf("\tRound alg. Init : %.3fs (%.2f%%)\n", time_alg_init, time_alg_init*100/time_total);
   printf("\tRound alg. B    : %.3fs (%.2f%%)\n", time_alg_b, time_alg_b*100/time_total);
   printf("\tRound alg. A    : %.3fs (%.2f%%)\n", time_alg_a, time_alg_a*100/time_total);
   printf("\tTotal time      : %.3fs (%.2f%%)\n", time_total, time_total*100/time_total);
}

void print_hex(const uint8_t *bytes, size_t length) {
  for(size_t i = 0; i < length; i++){
    printf("%02x", bytes[i]);
  }
  printf("\n");
}

void print_hex_short(const uint8_t *bytes, size_t length) {
  for(size_t i = 0; i < MAX; i++){
    printf("%02x", bytes[i]);
  }
  printf("...");
  for(size_t i = length - MAX; i < length; i++){
    printf("%02x", bytes[i]);
  }
  printf("\n");
}

void concat_keys(const uint8_t *key1, const uint8_t *key2, const uint8_t *key3,
                 size_t length, uint8_t *out) {
  memcpy(out, key1, length);
  memcpy(out + length, key2, length);
  memcpy(out + 2*length, key3, length);
}

int main(void) {
  char algos[4][100] = {
    OQS_KEM_alg_classic_mceliece_6688128,
    OQS_KEM_alg_ntru_hps4096821,
    OQS_KEM_alg_saber_firesaber,
    OQS_KEM_alg_kyber_1024
  };

  for (int i = 0; i < 4; i++) {
    clock_t begin_init = times(NULL);
    OQS_KEM *kem = OQS_KEM_new(algos[i]);
    printf("[--] Setting %s...\n", algos[i]);
    printf("[--] Public key bytes: %zu\n[--] Ciphertext bytes: %zu\n[--] Secret key bytes: %zu\n[--] Shared secret key bytes: %zu\n[--] NIST level: %d\n[--] IND-CCA: %s\n", kem->length_public_key, kem->length_ciphertext, kem->length_secret_key, kem->length_shared_secret, kem->claimed_nist_level, kem->ind_cca ? "Y" : "N");
    clock_t end_init = times(NULL);

    // Static keys for U_A
    uint8_t *ekA1 = malloc(kem->length_public_key);
    uint8_t *dkA1 = malloc(kem->length_secret_key);
    OQS_KEM_keypair(kem, ekA1, dkA1);

    printf("\n[U_A] Generating static keys...\n");
    printf("[U_A] ekA1: ");
    print_hex_short(ekA1, kem->length_public_key);
    printf("[U_A] dkA1: ");
    print_hex_short(dkA1, kem->length_secret_key);

    // Static keys for U_B
    uint8_t *ekB1 = malloc(kem->length_public_key);
    uint8_t *dkB1 = malloc(kem->length_secret_key);
    OQS_KEM_keypair(kem, ekB1, dkB1);

    printf("\n[U_B] Generating static keys...\n");
    printf("[U_B] ekB1: ");
    print_hex_short(ekB1, kem->length_public_key);
    printf("[U_B] dkB1: ");
    print_hex_short(dkB1, kem->length_secret_key);

    clock_t end_static_keys = times(NULL);

    // -----------------------------------------------
    // Init key exchange

    uint8_t *rA1 = malloc(kem->length_shared_secret);
    OQS_randombytes(rA1, kem->length_shared_secret);

    uint8_t *tempA1 = malloc(kem->length_shared_secret + kem->length_secret_key);
    uint8_t *hashA1 = malloc(kem->length_shared_secret);
    memcpy(tempA1, rA1, kem->length_shared_secret);
    memcpy(tempA1 + kem->length_shared_secret, dkA1, kem->length_secret_key);
    OQS_SHA3_sha3_256(hashA1, tempA1, kem->length_shared_secret + kem->length_secret_key);

    uint8_t *cA1 = malloc(kem->length_ciphertext);
    uint8_t *kA1 = malloc(kem->length_shared_secret);
    OQS_KEM_encaps(kem, cA1, kA1, ekB1);

    uint8_t *ekA2 = malloc(kem->length_public_key);
    uint8_t *dkA2 = malloc(kem->length_secret_key);
    OQS_KEM_keypair(kem, ekA2, dkA2);

    printf("\n[U_A] Generating ekA2 and dkA2...\n");
    printf("[U_A] ekA2: ");
    print_hex_short(ekA2, kem->length_public_key);
    printf("[U_A] dkA2: ");
    print_hex_short(dkA2, kem->length_secret_key);

    clock_t end_alg_init = times(NULL);

    // -----------------------------------------------
    uint8_t *rB1 = malloc(kem->length_shared_secret);
    uint8_t *rB2 = malloc(kem->length_shared_secret);
    OQS_randombytes(rB1, kem->length_shared_secret);
    OQS_randombytes(rB2, kem->length_shared_secret);

    uint8_t *tempB1 = malloc(kem->length_shared_secret + kem->length_secret_key);
    uint8_t *hashB1 = malloc(kem->length_shared_secret);
    memcpy(tempB1, rB1, kem->length_shared_secret);
    memcpy(tempB1 + kem->length_shared_secret, dkA1, kem->length_secret_key);
    OQS_SHA3_sha3_256(hashB1, tempB1, kem->length_shared_secret + kem->length_secret_key);

    uint8_t *cB1 = malloc(kem->length_ciphertext);
    uint8_t *kB1 = malloc(kem->length_shared_secret);
    OQS_KEM_encaps(kem, cB1, kB1, ekA1);

    printf("[U_B] Generating kB1...\n");
    printf("[U_B] kB1: ");
    print_hex(kB1, kem->length_shared_secret);

    uint8_t *cB2 = malloc(kem->length_ciphertext);
    uint8_t *kB2 = malloc(kem->length_shared_secret);
    OQS_KEM_encaps(kem, cB2, kB2, ekA2);

    printf("[U_B] Generating kB2...\n");
    printf("[U_B] kB2: ");
    print_hex(kB2, kem->length_shared_secret);

    uint8_t *kA1_prime = malloc(kem->length_shared_secret);
    OQS_KEM_decaps(kem, kA1_prime, cA1, dkB1);

    printf("[U_B] Generating kA1...\n");
    printf("[U_B] kA1: ");
    print_hex(kA1, kem->length_shared_secret);

    uint8_t *concat_keysB = malloc(3*kem->length_shared_secret);
    uint8_t *skB = malloc(kem->length_shared_secret);
    concat_keys(kA1, kB1, kB2, kem->length_shared_secret, concat_keysB);
    OQS_SHA3_sha3_256(skB, concat_keysB, 3*kem->length_shared_secret);

    clock_t end_algB = times(NULL);

    // -----------------------------------------------

    uint8_t *kB1_prime = malloc(kem->length_shared_secret);
    OQS_KEM_decaps(kem, kB1_prime, cB1, dkA1);

    printf("\n[U_A] Generating kB1_prime...\n");
    printf("[U_A] kB1_prime: ");
    print_hex(kB1_prime, kem->length_shared_secret);

    uint8_t *kB2_prime = malloc(kem->length_shared_secret);
    OQS_KEM_decaps(kem, kB2_prime, cB2, dkA2);

    printf("[U_A] Generating kB2_prime...\n");
    printf("[U_A] kB2_prime: ");
    print_hex(kB2_prime, kem->length_shared_secret);

    uint8_t *concat_keysA = malloc(3*kem->length_shared_secret);
    uint8_t *skA = malloc(kem->length_shared_secret);
    concat_keys(kA1_prime, kB1_prime, kB2_prime, kem->length_shared_secret, concat_keysA);
    OQS_SHA3_sha3_256(skA, concat_keysA, 3*kem->length_shared_secret);

    clock_t end_algA = times(NULL);

    printf("\n[U_A] skA: ");
    print_hex(skA, kem->length_shared_secret);

    printf("[U_B] skB: ");
    print_hex(skB, kem->length_shared_secret);

    if(memcmp(skA, skB, kem->length_shared_secret) != 0){
      printf("[--] Key exchange error!\n");
      return OQS_ERROR;
    }

    printf("[--] Key exchange successful!\n");

    // // Delete secrets and free
    OQS_MEM_secure_free(dkA1, kem->length_secret_key);
    OQS_MEM_secure_free(dkA2, kem->length_secret_key);
    OQS_MEM_secure_free(dkB1, kem->length_secret_key);
    OQS_MEM_secure_free(kA1, kem->length_shared_secret);
    OQS_MEM_secure_free(kB1, kem->length_shared_secret);
    OQS_MEM_secure_free(kB2, kem->length_shared_secret);
    OQS_MEM_secure_free(kA1_prime, kem->length_shared_secret);
    OQS_MEM_secure_free(kB1_prime, kem->length_shared_secret);
    OQS_MEM_secure_free(kB2_prime, kem->length_shared_secret);
    OQS_MEM_secure_free(concat_keysA, 3*kem->length_shared_secret);
    OQS_MEM_secure_free(skA, kem->length_shared_secret);
    OQS_MEM_secure_free(concat_keysB, 3*kem->length_shared_secret);
    OQS_MEM_secure_free(skB, kem->length_shared_secret);
    OQS_MEM_secure_free(tempA1, kem->length_shared_secret + kem->length_secret_key);
    OQS_MEM_secure_free(tempB1, kem->length_shared_secret + kem->length_secret_key);
    OQS_MEM_secure_free(hashA1, kem->length_shared_secret);
    OQS_MEM_secure_free(hashB1, kem->length_shared_secret);
    OQS_MEM_secure_free(rA1, kem->length_shared_secret);
    OQS_MEM_secure_free(rB1, kem->length_shared_secret);
    OQS_MEM_secure_free(rB2, kem->length_shared_secret);

    // Free
    OQS_MEM_insecure_free(ekA1);
    OQS_MEM_insecure_free(ekA2);
    OQS_MEM_insecure_free(ekB1);
    OQS_MEM_insecure_free(cA1);
    OQS_MEM_insecure_free(cB1);
    OQS_MEM_insecure_free(cB2);
    OQS_KEM_free(kem);

    clock_t end_total = times(NULL);

    print_stats(begin_init,
                     end_init,
                     end_static_keys,
                     end_alg_init,
                     end_algB,
                     end_algA,
                     end_total);
   printf("----------------------------------------------------------------------------------------\n");

  }
  return OQS_SUCCESS;
}
