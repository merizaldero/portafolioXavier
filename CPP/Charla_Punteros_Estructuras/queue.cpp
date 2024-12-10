#include <iostream>
#include <queue>
using namespace std;

void evaluar_cola(queue<string> pila){
    cout << "Conteo de Cola: " << pila.size() << "\n"; 
    if(!pila.empty()){
        cout << "Siguiente Cola: " << pila.front() << "\n";
        cout << "Ultimo Cola: " << pila.back() << "\n";
    }
    cout << "\n";
}
int main(){
    queue<string> carros;
    evaluar_cola(carros);

    carros.push("Volvo");
    carros.push("BMW");
    carros.push("Ford");
    evaluar_cola(carros);

    carros.front() = "Andino";
    carros.back() = "Kia";
    evaluar_cola(carros);

    carros.pop();
    evaluar_cola(carros);

    while( carros.size() > 0 ){
        carros.pop();
    }
    evaluar_cola(carros);

    return 0;
}