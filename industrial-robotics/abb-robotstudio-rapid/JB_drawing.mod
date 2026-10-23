MODULE Module1
    ! ATR0030 Lab 2 - Jordan Brodie
    ! Draws a circle (Path_10) and the initials J (Path_20) and B (Path_30) on Paper1 with markerB.
    ! Target orientation [0,0.707,0.707,0] = marker pointing straight down; config [-1,-1,0,1] = Cfg3.
    ! Z = 0 -> pen on paper, Z = 10 -> pen lifted (UP targets, step 2.4.5)

    ! --- Circle targets (AutoPath around cylinder r = 70 mm, centre 148.5,105) ---

    CONST robtarget Target_10:=[[148.5,35,0],[0,0.707106781,0.707106781,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_20:=[[218.5,105,0],[0,0.707106781,0.707106781,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_30:=[[148.5,175,0.1],[0,0.707106781,0.707106781,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_40:=[[78.5,105,0.1],[0,0.707106781,0.707106781,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_50:=[[148.5,35,0.1],[0,0.707106781,0.707106781,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    
    ! --- Letter J targets (free targets, method 2) ---
    CONST robtarget Target_60:=[[96.373,122.697,0],[0,0.707106781,0.707106781,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_60up:=[[96.373,122.697,10],[0,0.707106781,0.707106781,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_70:=[[128.291,123.702,0],[0,0.707106781,0.707106781,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_80:=[[127.45,85.334,0],[0,0.707106781,0.707106781,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_90:=[[99.327,88.197,0],[0,0.707106781,0.707106781,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    
    
    
    ! --- Letter B targets (free targets, method 2) ---
    CONST robtarget Target_100:=[[153.65,126.951,0],[0,0.707106781,0.707106781,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_100up:=[[153.65,126.951,10],[0,0.707106781,0.707106781,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]]; 
    CONST robtarget Target_110:=[[176.968,128.117,0],[0,0.707106781,0.707106781,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_120:=[[169.847,106.303,0],[0,0.707106781,0.707106781,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_140:=[[169.849,106.04,0],[0,0.707106781,0.707106781,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_130:=[[156.283,105.762,0],[0,0.707106781,0.707106781,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_150:=[[172.387,86.337,0],[0,0.707106781,0.707106781,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_160:=[[158.109,85.033,0],[0,0.707106781,0.707106781,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_170:=[[154.681,128.259,0],[0,0.707106781,0.707106781,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    ! --- Extra points added to shape J (220-240) and B (250, 180-210) ---
    CONST robtarget Target_220:=[[129.862,99.321,0],[0,0.707106781,0.707106781,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_230:=[[120.736,81.348,0],[0,0.707106781,0.707106781,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_240:=[[107.716,81.075,0],[0,0.707106781,0.707106781,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_250:=[[179.813,123.004,0],[0,0.707106781,0.707106781,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_180:=[[180.068,115.515,0],[0,0.707106781,0.707106781,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_190:=[[176.304,110.207,0],[0,0.707106781,0.707106781,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_200:=[[177.546,99.997,0],[0,0.707106781,0.707106781,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_210:=[[179.316,92.92,0],[0,0.707106781,0.707106781,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    
    
    PROC main() ! Jordan Brodie entry point
Path_10;   ! draw the circle
Path_20;   ! draw the letter J
Path_30;   ! draw the letter B
MoveAbsJ calib_pos, v1000, z0, tool0;   ! return to calibration position (all joints 0)
Stop;   ! end of program
ENDPROC
    
    
    PROC Path_10() ! circle: two circular moves through four points
        MoveJ Target_10,v1000,z100,markerB\WObj:=Paper1;
        MoveC Target_20,Target_30,v1000,z100,markerB\WObj:=Paper1;
        MoveC Target_40,Target_50,v1000,z100,markerB\WObj:=Paper1;
    ENDPROC
    PROC Path_20() ! letter J
        MoveJ Target_60up,v1000,z0,markerB\WObj:=Paper1;   ! hover 10 mm above start of J
        MoveJ Target_60,v1000,z0,markerB\WObj:=Paper1;     ! pen down
        MoveJ Target_70,v1000,z0,markerB\WObj:=Paper1;     ! top bar
        MoveJ Target_220,v1000,z0,markerB\WObj:=Paper1;    ! stem
        MoveJ Target_80,v1000,z0,markerB\WObj:=Paper1;
        MoveJ Target_230,v1000,z0,markerB\WObj:=Paper1;    ! hook
        MoveJ Target_240,v1000,z0,markerB\WObj:=Paper1;
        MoveJ Target_90,v1000,z0,markerB\WObj:=Paper1;
    ENDPROC
    PROC Path_30() ! letter B
        MoveJ Target_100up,v1000,z0,markerB\WObj:=Paper1;  ! hover 10 mm above start of B
        MoveJ Target_100,v1000,z0,markerB\WObj:=Paper1;    ! pen down
        MoveJ Target_110,v1000,z0,markerB\WObj:=Paper1;    ! top
        MoveJ Target_250,v1000,z0,markerB\WObj:=Paper1;    ! upper bowl
        MoveJ Target_180,v1000,z0,markerB\WObj:=Paper1;
        MoveJ Target_190,v1000,z0,markerB\WObj:=Paper1;
        MoveJ Target_120,v1000,z0,markerB\WObj:=Paper1;
        MoveJ Target_140,v1000,z0,markerB\WObj:=Paper1;
        MoveJ Target_130,v1000,z0,markerB\WObj:=Paper1;    ! middle bar to stem
        MoveJ Target_140,v1000,z0,markerB\WObj:=Paper1;
        MoveJ Target_200,v1000,z0,markerB\WObj:=Paper1;    ! lower bowl
        MoveJ Target_210,v1000,z0,markerB\WObj:=Paper1;
        MoveJ Target_150,v1000,z0,markerB\WObj:=Paper1;
        MoveJ Target_160,v1000,z0,markerB\WObj:=Paper1;    ! bottom
        MoveJ Target_170,v1000,z0,markerB\WObj:=Paper1;    ! stem back up, closes the B
    ENDPROC
ENDMODULE