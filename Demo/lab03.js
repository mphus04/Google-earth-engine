const pr1 = {
    name : "ao thun ",
    price: 100
}
const pr2 = {
    name : "ao khoac ",
    price: 700
}
const pr3 = {
    name : "ao choang ",
    price: 300
}
const pr4 = {
    name : "quan thun ",
    price: 700
}
const pr5 = {
    name : "quan jean ",
    price: 900
}

const product = [pr1,pr2,pr3,pr4,pr5]
console.log("orinal",product);

console.log("san pham dau tien co ten : ",product[0].name);
const updateSP2 =  [pr1,{
        name :pr2.name,
        price: 180}
        ,pr3,pr4,pr5]
console.log(updateSP2,"mang sau cap nhat")
product.push({
    name: "last product",
    price: 800
})
console.log(product,"sau khi them sp");

product.pop()
console.log("remove sp cuoi",product);

product.forEach((item,index)=>{
    console.log(`product ${index} name =  `,item.name)
})

product.map((item,index)=>{
    console.log(`product ${index} price` ,item.price)
})