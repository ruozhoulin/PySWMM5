//-----------------------------------------------------------------------------
//   swmm5.h
//
//   Project: EPA SWMM5
//   Version: 5.1
//   Date:    03/24/14  (Build 5.1.001)
//            08/01/16  (Build 5.1.011)
//   Author:  L. Rossman
//
//   Prototypes for SWMM5 functions exported to swmm5.dll.
//
//-----------------------------------------------------------------------------

#ifndef SWMM5_H
#define SWMM5_H


// --- define WINDOWS

#undef WINDOWS
#ifdef _WIN32
  #define WINDOWS
#endif
#ifdef __WIN32__
  #define WINDOWS
#endif

// --- define DLLEXPORT

#ifdef WINDOWS
    #define DLLEXPORT __declspec(dllexport) __stdcall
#else
    #define DLLEXPORT
#endif

// --- use "C" linkage for C++ programs

#ifdef __cplusplus
extern "C" {
#endif

int  DLLEXPORT   swmm_run(char* f1, char* f2, char* f3);
int  DLLEXPORT   swmm_open(char* f1, char* f2, char* f3);
int  DLLEXPORT   swmm_start(int saveFlag);
int  DLLEXPORT   swmm_step(double* elapsedTime);
int  DLLEXPORT   swmm_end(void);
int  DLLEXPORT   swmm_report(void);
int  DLLEXPORT   swmm_getMassBalErr(float* runoffErr, float* flowErr,
                 float* qualErr);
int  DLLEXPORT   swmm_close(void);
int  DLLEXPORT   swmm_getVersion(void);
int  DLLEXPORT   swmm_getError(char* errMsg, int msgLen);
int  DLLEXPORT   swmm_getWarnings(void);

//-----------------------------------------------------------------------------
//   Project:  SWMM Toolbox based on SWMM 5.1.015
//   Version:  0.0.1
//   Date:     05/31/2021
//   Author:   Ruozhou Lin
//	 Email:	   ruozhoulin@zju.edu.cn
//
//	 Constants and functions used by api_hy.c
//
//-----------------------------------------------------------------------------

int  DLLEXPORT   swmm_run_sqlite(char* f1, char* f2, char* f3);
int  DLLEXPORT   swmm_end_csv(void);
int  DLLEXPORT   swmm_report_sqlite(void);

//
int  DLLEXPORT   swmm_run_open(char* f1, char* f2, char* f3);
int  DLLEXPORT   swmm_run_simulation();
int  DLLEXPORT   swmm_run_close();

// read result
double DLLEXPORT result_system_total_flood(void);







#ifdef __cplusplus
}   // matches the linkage specification from above */
#endif


#endif //SWMM5_H
