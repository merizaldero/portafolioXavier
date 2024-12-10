#include <iostream>
#include <vector>
using namespace std;

int main(){
    vector<string> carros = {"Volvo", "BMW", "Ford", "Mazda"};
    
    if(carros.empty() ){
        cout << "El vector esta vacio";
    } else {
        for (int i = 0; i < carros.size(); i++) {
            cout << carros[i] << " ";
        }
        cout << "\n";
    }

    cout << carros.front() << " es el primer elemento\n";
    cout << carros.back() << " es el ultimo elemento\n";
    cout << carros.at(1) << " esta en la posicion 1\n";
    cout << carros.at(2) << " esta en la posición 2\n";

    carros[0] = "Opel";
    carros.at(2) = "Andino";

    carros.push_back("Tesla");
    carros.push_back("VW");

    cout << "El ultimo elemento es " << carros.back() << "\n";
    carros.pop_back();
    cout << "Ahora, el ultimo elemento es " << carros.back() << "\n";

    for (string car : carros) {
        cout << car << " ";
    }
    cout << "\n";

    return 0;
}