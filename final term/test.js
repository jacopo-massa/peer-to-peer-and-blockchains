const BoxIncomplete = artifacts.require("BoxIncomplete");
const IncreasingPenalty = artifacts.require("IncreasingPenalty")

// addresses are hard-coded because I didn't use web3 library.
let a = "0x1047a18b68a7c860b3447f8D9271C3a616a257ac"
let b = "0xDea453288AFB975D269E1C26f74120C1E6964900"
let c = "0x014eeD0cbaF7E20E6941a99B1Fd28C418Ff59Da6"

let producer_price = 50000000000000000;
let transporter_price = 75000000000000000;

contract("BoxIncomplete", async accounts => {
	
  	it("Testing all ok", async () => {

  		const pf = await IncreasingPenalty.deployed();
  		const instance = await BoxIncomplete.new(b,c,pf.address);

  		const result = await instance.ship({from:b, value:producer_price})
  		console.log("Ship: " + result.receipt.gasUsed);

  		let temp = [35, 30, 35, 40, 38, 35, 30, 35, 40, 38, 35, 30, 35, 40, 38, 35, 30, 35, 40, 38, 35, 30, 35, 40, 38, 35, 30, 35, 40, 38, 35, 30, 35, 40, 38, 35, 30, 35, 40, 38, 35, 30, 35, 40, 38, 35, 30, 35, 40, 38, 35, 30, 35, 40, 38, 35, 30, 35, 40, 38, 35, 30, 35, 40, 38, 35, 30, 35, 40, 38, 35, 30, 35, 40, 38, 35, 30, 35, 40, 38, 35, 30, 35, 40, 38, 35, 30, 35, 40, 38, 35, 30, 35, 40, 38, 37]
  		let bump = [3000, 3500, 3200, 4000, 2000, 3000, 3500, 3200, 4000, 2000, 3000, 3500, 3200, 4000, 2000, 3000, 3500, 3200, 4000, 2000, 3000, 3500, 3200, 4000, 2000, 3000, 3500, 3200, 4000, 2000, 3000, 3500, 3200, 4000, 2000, 3000, 3500, 3200, 4000, 2000, 3000, 3500, 3200, 4000, 2000, 3000, 3500, 3200, 4000, 2000, 3000, 3500, 3200, 4000, 2000, 3000, 3500, 3200, 4000, 2000, 3000, 3500, 3200, 4000, 2000, 3000, 3500, 3200, 4000, 2000, 3000, 3500, 3200, 4000, 2000, 3000, 3500, 3200, 4000, 2000, 3000, 3500, 3200, 4000, 2000, 3000, 3500, 3200, 4000, 2000, 2000, 3000, 3500, 3200, 4000, 2000]

  		const result2 = await instance.push_data(temp, bump, {from:b})
  		console.log("Push_Data: " + result2.receipt.gasUsed);

  		const result3 = await instance.complete({from: c, value:transporter_price})
  		console.log("Complete: " + result3.receipt.gasUsed);
  	});

  	it("Testing not ok", async () => {

  		const pf = await IncreasingPenalty.deployed();
  		const instance = await BoxIncomplete.new(b,c,pf.address);

  		const result = await instance.ship({from:b, value:producer_price})
  		console.log("Ship: " + result.receipt.gasUsed);

  		let temp = [50, 50, 50, 60, 55, 55, 60, 55, 50, 50, 50, 60, 55, 55, 60, 55, 50, 50, 50, 60, 55, 55, 60, 55, 50, 50, 50, 60, 55, 55, 60, 55, 50, 50, 50, 60, 55, 55, 60, 55, 50, 50, 50, 60, 55, 55, 60, 55, 50, 50, 50, 60, 55, 55, 60, 55, 50, 50, 50, 60, 55, 55, 60, 55, 50, 50, 50, 60, 55, 55, 60, 55, 50, 50, 50, 60, 55, 55, 60, 55, 50, 50, 50, 60, 55, 55, 60, 55, 50, 50, 50, 60, 55, 55, 60, 55]
        let bump = [20000, 40000, 20000, 8000, 20000, 20000, 20000, 80000, 20000, 40000, 20000, 8000, 20000, 20000, 20000, 80000, 20000, 40000, 20000, 8000, 20000, 20000, 20000, 80000, 20000, 40000, 20000, 8000, 20000, 20000, 20000, 80000, 20000, 40000, 20000, 8000, 20000, 20000, 20000, 80000, 20000, 40000, 20000, 8000, 20000, 20000, 20000, 80000, 20000, 40000, 20000, 8000, 20000, 20000, 20000, 80000, 20000, 40000, 20000, 8000, 20000, 20000, 20000, 80000, 20000, 40000, 20000, 8000, 20000, 20000, 20000, 80000, 20000, 40000, 20000, 8000, 20000, 20000, 20000, 80000, 20000, 40000, 20000, 8000, 20000, 20000, 20000, 80000, 20000, 40000, 20000, 8000, 20000, 20000, 20000, 80000]

  		const result2 = await instance.push_data(temp, bump, {from:b})
  		console.log("Push_Data: " + result2.receipt.gasUsed);

  		const result3 = await instance.complete({from: c, value:transporter_price})
  		console.log("Complete: " + result3.receipt.gasUsed);
  	});

  	it("Testing some ok some not", async () => {

  		const pf = await IncreasingPenalty.deployed();
  		const instance = await BoxIncomplete.new(b,c,pf.address);

  		const result = await instance.ship({from:b, value:producer_price})
  		console.log("Ship: " + result.receipt.gasUsed);

  		let temp = [35, 40, 50, 55, 45, 35, 40, 50, 55, 45, 35, 40, 50, 55, 45, 35, 40, 50, 55, 45, 35, 40, 50, 55, 45, 35, 40, 50, 55, 45, 35, 40, 50, 55, 45, 35, 40, 50, 55, 45, 35, 40, 50, 55, 45, 35, 40, 50, 55, 45, 35, 40, 50, 55, 45, 35, 40, 50, 55, 45, 35, 40, 50, 55, 45, 35, 40, 50, 55, 45, 35, 40, 50, 55, 45, 35, 40, 50, 55, 45, 35, 40, 50, 55, 45, 35, 40, 50, 55, 45, 45, 35, 40, 50, 55, 45]
        let bump = [3000, 3500, 5500, 4000, 6000, 3000, 3500, 5500, 4000, 6000, 3000, 3500, 5500, 4000, 6000, 3000, 3500, 5500, 4000, 6000, 3000, 3500, 5500, 4000, 6000, 3000, 3500, 5500, 4000, 6000, 3000, 3500, 5500, 4000, 6000, 3000, 3500, 5500, 4000, 6000, 3000, 3500, 5500, 4000, 6000, 3000, 3500, 5500, 4000, 6000, 3000, 3500, 5500, 4000, 6000, 3000, 3500, 5500, 4000, 6000, 3000, 3500, 5500, 4000, 6000, 3000, 3500, 5500, 4000, 6000, 3000, 3500, 5500, 4000, 6000, 3000, 3500, 5500, 4000, 6000, 3000, 3500, 5500, 4000, 6000, 3000, 3500, 5500, 4000, 6000, 6000, 3000, 3500, 5500, 4000, 6000]

  		const result2 = await instance.push_data(temp, bump, {from:b})
  		console.log("Push_Data: " + result2.receipt.gasUsed);

  		const result3 = await instance.complete({from: c, value:transporter_price})
  		console.log("Complete: " + result3.receipt.gasUsed);
  	});
});


