unknownVariableAtTranspileTime = 0

obj = { method1: () => console.log("hello world") }
if (unknownVariableAtTranspileTime) {
    obj.method1 = () => console.log("new function")
}
obj.method1()