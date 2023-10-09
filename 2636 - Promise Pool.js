var start = performance.now();
/**
 * @param {Function[]} functions
 * @param {number} n
 * @return {Promise<any>}
 */
var promisePool = async function (functions, n) {
  function promisePoolRecursive(config) {
    if (config.n > 0 && config.index <= config.functions.length - 1) {
      config.n--;
      config.functions[config.index++]().then(() => {
        config.n++;
        console.log('Promise resolved -', performance.now() - start);
        promisePoolRecursive(config);
      });
      promisePoolRecursive(config);
    }
  }
  promisePoolRecursive({ functions, n, index: 0 });
};

const sleep = t => new Promise(res => setTimeout(res, t));

const functions = [
  () => new Promise(res => setTimeout(res, 300)),
  () => new Promise(res => setTimeout(res, 400)),
  () => new Promise(res => setTimeout(res, 200))
];

(async () => {
  promisePool(functions, 2);
})();
