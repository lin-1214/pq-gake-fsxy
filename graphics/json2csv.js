const fs = require("fs");
const process = require("process");

const array_chunks = (array, chunk_size) => Array(Math.ceil(array.length / chunk_size)).fill().map((_, index) => index * chunk_size).map(begin => array.slice(begin, begin + chunk_size));

var isTTY = process.stdin.isTTY;
var stdin = process.stdin;
var stdout = process.stdout;

type = process.argv[2];
N = process.argv[3];
// If no STDIN and no arguments, display usage message
if (isTTY && args.length !== 0) {
    handleShellArguments();
}
// read from STDIN
else {
    handlePipedContent();
}

function handlePipedContent() {
    var data = '';

    stdin.on('readable', function() {
        var chuck = stdin.read();
        if(chuck !== null){
            data += chuck;
        }
    });
    stdin.on('end', function() {
      let header = "type,algorithm,operation,iterations,total_time_s,mean_time_us,pop_stdev,mean_cpu_cycles";
      if (type === "gake") header += `,N`
      stdout.write(header + "\n");
      stdout.write(
        array_chunks(
          JSON.parse(data).slice(1), type !== "gake" ? 4 : 5).map(x => {
            alg = x[0].Operation;
            return x.slice(1).map(
              y => ({alg, ...y})
            )
          }
        ).flat()
         .map(x => {
           str = `${type},${x.alg},${x.Operation},${x.Iterations},${x["Total time (s)"]},${x["Time (us): mean"]},${x["pop. stdev"]},${x["CPU cycles: mean"]}`
           if (type === "gake") str += `,${N}`
           return str
         })
         .join("\n") + "\n"
      )
    });
}
