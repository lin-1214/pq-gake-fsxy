#include <time.h>
#include <sys/times.h>
#include <unistd.h>

void print_stats(clock_t begin_init,
                 clock_t end_init,
                 clock_t end_keys,
                 clock_t end_alg_init,
                 clock_t end_algB,
                 clock_t end_algA,
                 clock_t end_total);

void print_hex(const uint8_t *bytes, size_t length);
void print_hex_short(const uint8_t *bytes, size_t length, size_t max);
void print_short_key_sep(const uint8_t *key, size_t length, size_t show, char* sep);
void init_to_zero(uint8_t *key, int length);
