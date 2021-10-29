ENABLED_ALGS=OQS_ENABLE_KEM_kyber_1024

git clone https://github.com/jiep/liboqs
cd liboqs
git checkout coins

mkdir -p build
cd build
rm -rf *
cmake -GNinja -DOQS_MINIMAL_BUILD="${ENABLED_ALGS}" ..
ninja
