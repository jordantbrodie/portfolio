clear; clc; close all
%% Jordan Thomas Brodie | 243483 | ATR0030 | RPR8
% Builds on the transformation chain in my FK and WS reports.
L0=3; L1=5; L2max=6; L3=5;
T01H=trvec2tform([0 0 L0]);
R01H=axang2tform([0 1 0 -pi/2]);
T12H=trvec2tform([L1 0 0]);
T3EH=trvec2tform([0 L3 0]);


TARGET=[6 5 8]; % Starting target: my home EE position


d=0.05; % Coordinate-wise tolerance, as in the manual


N=72; % Includes 0, 90 and 180 degrees; no repeated 360-degree endpoint
rangeA=(0:N-1)*2*pi/N;
rangeB=(0:N-1)*2*pi/N;
rangeL=linspace(L2max,0,21);
configs=zeros(3,0); errors=zeros(1,0); cnt=0;
figure('Color','w'); hold on; grid on; axis equal; view(45,30)
xlabel('x'); ylabel('y'); zlabel('z');
plot3(TARGET(1),TARGET(2),TARGET(3),'rp','MarkerSize',14,'LineWidth',2);
colors=lines(12);


% Cache transformations: avoid toolbox conversion calls inside the search.
J1cache=zeros(4,4,N); J2cache=zeros(4,4,N); R3cache=zeros(4,4,N);
for k=1:N
    J1cache(:,:,k)=T01H*R01H*axang2tform([0 0 1 rangeA(k)]);
    J2cache(:,:,k)=J1cache(:,:,k)*T12H;
    R3cache(:,:,k)=axang2tform([0 0 1 rangeB(k)]);
end
fprintf('Searching %d configurations...\n',numel(rangeL)*N*N);
tic
for L2=rangeL
    t2h=trvec2tform([0 0 -L2]);
    for ib=1:N
        B=rangeB(ib); r3h=R3cache(:,:,ib);
        for ia=1:N
            A=rangeA(ia);
            J1=J1cache(:,:,ia);
            J2=J2cache(:,:,ia);
            J3=J2*t2h;
            EE=J3*r3h*T3EH;
            PE=EE(1:3,4).';
            if all(abs(PE-TARGET)<d)
                P1=J1(1:3,4).'; P2=J2(1:3,4).';
                P3=J3(1:3,4).';
                cnt=cnt+1;
                configs(:,cnt)=[rad2deg(A); rad2deg(B); L2];
                errors(cnt)=norm(PE-TARGET);
                C=colors(mod(cnt-1,size(colors,1))+1,:);
                P=[0 0 0; P1; P2; P3; PE];
                plot3(P(:,1),P(:,2),P(:,3),'-o','Color',C,'LineWidth',1.5);


                % J3 frame includes the final revolute joint rotation.
                frames={J1,J2,J3*r3h,EE};
                names={'J1','J2','J3','EE'};
                for k=1:4
                    F=frames{k};
                    plotTransforms(tform2trvec(F),tform2quat(F),'FrameSize',0.7);
                    text(F(1,4),F(2,4),F(3,4),[' ' names{k}]);
                end
            end
        end
    end
end
fprintf('Search completed in %.2f seconds.\n',toc);
title(sprintf('Jordan Brodie RPR8 IK: %d sampled configurations',cnt));
fprintf('Rows: A (deg), B (deg), L2; each column is one configuration.\n');
disp(configs)
fprintf('Euclidean EE errors (coordinate-wise acceptance used):\n'); disp(errors)
if cnt==0
    warning('No sampled solution: check reachability, grid spacing and tolerance.');
end
exportgraphics(gcf,'JordanBrodie_IK_configurations.jpg','Resolution',200);
save('JordanBrodie_IK_results.mat','configs','TARGET','d','N','errors');
