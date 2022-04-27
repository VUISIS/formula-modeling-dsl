# Formula Modeling DSL

The Intermediate.dsl file defines a DSL for Formula that represents general
application structure relationships, and can be used as an intermediate representation
of languages like AADL, SysML2 and others. The goal is to be able to convert
various models into a common DSL that can be used to reason about the models.

## aadl_to_intermediate
The aadl_to_intermediate utility is a simplistic Python script that uses regular
expressions to match patterns in an AADL file and generate an intermediate file.
To run it, just supply an input AADL filename and an output 4ML filename:
```
python3 aadl_to_intermediate.py missile_guidance_v5.aadl guidance.4ml
```
