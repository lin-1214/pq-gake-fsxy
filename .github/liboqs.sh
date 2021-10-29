ENABLED_ALGS=OQS_ENABLE_KEM_kyber_1024

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  sudo apt update
  sudo apt install -y ninja-build zip build-essential cmake libssl-dev
elif [[ "$OSTYPE" == "darwin"* ]]; then
  brew install ninja gnu-tar zip cmake openssl@1.1
else
  exit 0
fi

git clone https://github.com/jiep/liboqs
cd liboqs
git checkout coins

mkdir -p build
cd build
rm -rf *
cmake -GNinja -DOQS_MINIMAL_BUILD="${ENABLED_ALGS}" ..
ninja
