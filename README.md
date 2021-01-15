# OpenLostCat - Open Logic-based Simple Tag-bundle Categorizer

## Base idea and motivation


## Getting started

## Demo

## Details

### Elements (classes)
#### Operators
Basically operators works as filter. Every operator has an apply function which get a list of tags and produces a subset of this list.

##### AtomicFilter
It checks whether a key is presented in the tags list and the value of the tag meets with the desirable values. It returns with the filtered set.

attributes: 

 - key: the name of the tag which has to be investigated
 - values: the possibly values of the tags

methods
 - apply
 - init: a tuple of key and value
 ```
op = Sipmle(("key", ["value1", "value2"]))
```

Key could be

Values could be a single value or a list of single values.

More detail see the Syntax.

If null is presented in the list means that the key is not mandatory to be presented in the tags but it is than the values can be only in the values set.

If null is the 

##### FilterNOT
FilterNOT can be use as negation. It provides the complementary set of the underlying operator result.

attributes: 

 - one operator

methods
 - apply
 - init:
```
op = Sipmle(("key", ["value1", "value2"]))
FilterNOT(op)
```


##### FilterAND
##### FilterOR
##### BoolConst
#### Category
#### CategoryCatalog


### Syntax
The Sytax or categories file. JSON file format is used so it must be a valid JSON file.

CategoryCatalog ::= Category | [Category, ...]
Category ::= BoolConst | FilterAND (Rule with a restriction to FilterAND) | [Rule, ...]
BoolConst ::= bool (true | false)
Rule ::= FilterAND | FilterOR
FilterNOT ::= FilterAND | FilterOR
FilterOR ::= [FilterAND | FilterOR, ...]
FilterAND ::= {Tuple, ...}
Tuple ::= "__AND..." : FilterAND | "__OR..." : FilterOR | "__NOT..." : FilterNOT | SimpleOp
SimpleOp ::= str (starts not with "__AND", "__OR", "__NOT") : SingleValue | [SingleValue, ...]
SingleValue ::= bool | str | int | null


where
 - bool, str, int, null : the corresponding json type
 - [x,..]  :  json list of elements x
 - {tuple,.. }  : json dict elements of tuples  /(key, value) pairs/
 - x | y : x or y elements can be presented here
 - (...) : some additional notes
 - "txt..." : json string which starts by "txt"
 
SingleValue conversions in AtomicFilter operator:

 - bool: "yes" if true; "no" if false
 - str: str
 - int: string representation of int 
 - null: it means that the key must not be represented in the tag list

