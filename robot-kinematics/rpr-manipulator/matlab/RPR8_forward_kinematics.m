clear; clc; close all

%% Jordan Brodie - RPR8 Forward Kinematics

% Link lengths - Variant 8
L0 = 3;
L1 = 5;
L2max = 6;
L3 = 5;

%% Translation and reorientation vectors

% J0 -> J1
T01 = [0 0 L0];

% Rotate J0 frame around y-axis to obtain J1 frame
R01 = [0 1 0 -pi/2];

% J1 -> J2: travel 5 units along local +x
T12 = [L1 0 0];

% J2 -> J3: travel 6 units along local -z
% L2 is the prismatic link for RPR8
T23 = [0 0 -L2max];

% J3 -> End Effector: travel 5 units along local +y
T3E = [0 L3 0];

%% Convert to homogeneous transformation matrices

T01H = trvec2tform(T01);
R01H = axang2tform(R01);
T12H = trvec2tform(T12);
T23H = trvec2tform(T23);
T3EH = trvec2tform(T3E);

%% RPR8 geometry model

J1 = T01H * R01H;
J2 = J1 * T12H;
J3 = J2 * T23H;
EE = J3 * T3EH;

%% Position vectors

P1 = tform2trvec(J1);
P2 = tform2trvec(J2);
P3 = tform2trvec(J3);
PE = tform2trvec(EE);

%% Display joint positions

fprintf('        P1        P2        P3        PE\n')
disp([P1(:) P2(:) P3(:) PE(:)])

%% Plot RPR8 manipulator

windowFunction;
title('Jordan Brodie RPR8 Forward Kinematics')

linksFunction(P1,P2,P3,PE)
labelsFunction(P1,P2,P3,PE)
framesFunction(J1,J2,J3,EE)


%% =========================================================
% USER-DEFINED FUNCTIONS
% ==========================================================

%% Figure window
function windowFunction

    plot3(0,0,0,'o')

    hold on
    grid on
    axis equal

    xlabel('x')
    ylabel('y')
    zlabel('z')

    view(3)

end


%% Plot links
function linksFunction(P1,P2,P3,PE)

    % J0 -> J1
    plot3([0 P1(1)], ...
          [0 P1(2)], ...
          [0 P1(3)], ...
          'b-.','LineWidth',1.5)

    % J1 -> J2
    plot3([P1(1) P2(1)], ...
          [P1(2) P2(2)], ...
          [P1(3) P2(3)], ...
          'b-.','LineWidth',1.5)

    % J2 -> J3
    plot3([P2(1) P3(1)], ...
          [P2(2) P3(2)], ...
          [P2(3) P3(3)], ...
          'r-.','LineWidth',1.5)

    % J3 -> End Effector
    plot3([P3(1) PE(1)], ...
          [P3(2) PE(2)], ...
          [P3(3) PE(3)], ...
          'g-.','LineWidth',1.5)

end


%% Plot joint labels
function labelsFunction(P1,P2,P3,PE)

    d = 0.2;

    text(d,0,0,'J0')

    text(P1(1)+d, ...
         P1(2), ...
         P1(3)-d, ...
         'J1')

    text(P2(1)+d, ...
         P2(2), ...
         P2(3)-d, ...
         'J2')

    text(P3(1)+d, ...
         P3(2), ...
         P3(3)-d, ...
         'J3')

    text(PE(1)+d, ...
         PE(2), ...
         PE(3)-d, ...
         'EE')

end


%% Plot coordinate frames
function framesFunction(J1,J2,J3,EE)

    plotTransforms( ...
        tform2trvec(J1), ...
        tform2quat(J1))

    plotTransforms( ...
        tform2trvec(J2), ...
        tform2quat(J2))

    plotTransforms( ...
        tform2trvec(J3), ...
        tform2quat(J3))

    plotTransforms( ...
        tform2trvec(EE), ...
        tform2quat(EE))

end