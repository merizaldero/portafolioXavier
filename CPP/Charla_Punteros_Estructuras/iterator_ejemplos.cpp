#include <iostream>
#include <list>
#include <deque>
#include <set>
#include <map>
using namespace std;

int main(){

    cout << "Iterando List\n";
    // Create a list called cars that will store strings
    list<string> lista = {"Volvo", "BMW", "Ford", "Mazda"};
    // Loop through the list with an iterator
    for (auto it = lista.begin(); it != lista.end(); ++it) {
        cout << *it << " ";
    }
    cout << "\n";

    cout << "Iterando Deque\n";
    // Create a deque called cars that will store strings
    deque<string> midequeue = {"Volvo", "BMW", "Ford", "Mazda"};
    // Loop through the deque with an iterator
    for (auto it = midequeue.begin(); it != midequeue.end(); ++it) {
        cout << *it << " ";
    }
    cout << "\n";

    cout << "Iterando Set\n";
    // Create a set called cars that will store strings
    set<string> miset = {"Volvo", "BMW", "Ford", "Mazda"};
    // Loop through the set with an iterator
    for (auto it = miset.begin(); it != miset.end(); ++it) {
        cout << *it << " ";
    }
    cout << "\n";

    cout << "Iterando Map\n";
    // Create a map that will store strings and integers
    map<string, int> mapa = { {"John", 32}, {"Adele", 45}, {"Bo", 29} };
    // Loop through the map with an iterator
    for (auto it = mapa.begin(); it != mapa.end(); ++it) {
        cout << it->first << " : " << it->second << ", ";
    }
    cout << "\n";

    return 0;
}