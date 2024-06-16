=====
Usage
=====

To use carbatpy in a project::

    import carbatpy
    
The name of the results directory is stored in **cb_config.py** in _RESULTS_DIR.
It is set to the value of environment variable *CARBATPY_RES_DIR*. Also the name
of the directories with the Refprop (NIST) installation are set there. At the
moment carbatpy needs a *Refprop* license!
Finally an environment variable name with the base directory is used
*CARBATPY_BASE_DIR*
    
You may want to check the test files and the files in the src/models folder
and in the src/utils folder (e.g. run_heat_pump_simple).