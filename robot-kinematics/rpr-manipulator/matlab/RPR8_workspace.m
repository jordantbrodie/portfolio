clear; clc; close all
 
%% From JordanBrodie_FK.m
% Link lengths - RPR8
L0=3; L1=5; L2max=6; L3=5; 
 
% Offset and reorientation vectors - RPR8
% Same geometry as the verified RPR8 Forward Kinematics model

% J0 -> J1: translation along base +z
T01=[0 0 L0];

% Rotate J0 frame -pi/2 around y-axis to obtain J1 frame
R01=[0 1 0 -pi/2];

% J1 -> J2: translation along local +x
T12=[L1 0 0];

% J3 -> EE: translation along local +y
T3E=[0 L3 0];

% Their homogeneous matrices 
T01H=trvec2tform(T01);
R01H=axang2tform(R01);
T12H=trvec2tform(T12);
T3EH=trvec2tform(T3E);

%% Tolerance and joint limits
d=0.05; % tolerance

% Joint limits to prevent floor collision
% A is limited so J3, L3 and EE remain above floor
% for the complete 360 degree rotation of B
minA=-1.148;
maxA= 1.148;

% B can complete one full revolution
minB=0;
maxB=2*pi;

% RPR8 prismatic joint L2
minL=0; maxL=L2max;

% Number of cycles and ranges
N=20;

rangeA=linspace(minA, maxA, N);
rangeB=linspace(minB, maxB, N);
rangeL=linspace(maxL, minL, N);

% Container of EE poses and message
poses=[]; msg='';

%% Jordan Brodie RPR8 kinematics model
for L2=rangeL % or 0 to stop L
for B=rangeB  % or 0 to stop B
for A=rangeA  % or 0 to stop A

% Jordan Brodie variable A,B,L parameters
% RPR8 = Revolute - Prismatic - Revolute

% First revolute joint A
% Rotation around the local z-axis of J1
r1=[0 0 1 A];

% Prismatic joint L2
% In the home FK model J2 -> J3 is along local -z
t2=[0 0 -L2];

% Final revolute joint B
% Rotation around the local z-axis of J3
r3=[0 0 1 B];

% Convert variable parameters to homogeneous matrices
r1h=axang2tform(r1);
t2h=trvec2tform(t2);
r3h=axang2tform(r3);

% RPR8 model considering variable parameters
%
% Home model from FK:
% J1 = T01H * R01H
% J2 = J1 * T12H
% J3 = J2 * T23H
% EE = J3 * T3EH
%
% Workspace model inserts A, L2 and B into this chain.

% First revolute joint
J1=T01H * R01H * r1h;

% Fixed link L1
J2=J1 * T12H;

% Prismatic joint L2
J3=J2 * t2h;

% Final revolute joint B and fixed link L3
EE=J3 * r3h * T3EH;

% Joint and EE positions
P1=tform2trvec(J1);
P2=tform2trvec(J2);
P3=tform2trvec(J3);
PE=tform2trvec(EE);


%% Collecting EE positions

% Checking if EE collides with floor
collision=PE(3)<d;

if collision

    msg=sprintf( ...
        'EE can collide with floor at z=%.2f, A=%.2f, B=%.2f, L2=%.2f', ...
        PE(3),A,B,L2);

else

    % Checking if J3 goes below the floor
    collision=P3(3)<d;

    if collision

        msg=sprintf( ...
            'J3 can collide with floor at z=%.2f, A=%.2f, B=%.2f, L2=%.2f', ...
            P3(3),A,B,L2);

    end
end

% Save only collision-free EE positions
if ~collision
    poses=[poses, PE(:)];
end

end
end
end

%% Functions that can be called to explore workspace
if isempty(msg)
    disp('No collisions detected.')
else
    disp('Collision configurations were detected and removed from the workspace.')
    disp(msg)
end

x=poses(1,:);
y=poses(2,:);
z=poses(3,:);

% 3D workspace
figure;
windowFunction;
title('Jordan Brodie RPR8 workspace')
surface([x; x], [y; y], [z; z], ...
    'EdgeColor', 'interp')
view(45,30)


% XY view
figure;
windowFunction;
title('Jordan Brodie RPR8 XY view')
surface([x; x], [y; y], [z; z], ...
    'EdgeColor', 'interp')
view(2)

% XZ view
figure;
windowFunction;
title('Jordan Brodie RPR8 XZ view')
surface([x; x], [y; y], [z; z], ...
    'EdgeColor', 'interp')
view(1,1)

% YZ view
figure;
windowFunction;
title('Jordan Brodie RPR8 YZ view')
surface([x; x], [y; y], [z; z], ...
    'EdgeColor', 'interp')
view(90,1)

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

end