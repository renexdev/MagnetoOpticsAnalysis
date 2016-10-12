%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%"Rene Cejas Bolecek\n\
%reneczech@gmail.com / ncejas@cab.cnea.gov.ar\n\
%Low Temperatures Laboratory, Centro Atomico Bariloche\n\
%Instituto Balseiro, Universidad Nacional de Cuyo\n\
%Avenida Bustillo 9500, 8400 Bariloche, Rio Negro, Argentina\n\
%MIT License\n\
%"
%
%Output: save Intensity vs H  in selected square AREA \n\
%Input: images source\n"
%LastUpdate: 12/10/16
%%%%%%%%%%%%%%/%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
close all;
clear all;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Info given by user
flag_loop_pick_pics = 0;
% 0: All pics (default)
% Number >=1 pics from 1 to N

flag_show_profiles = 1;
%1: Display profiles
%0: Turn off display (default)

loopId = 2; 
%1: Rising field
%2: Decreasing field

fileformat='*.tif' 

%Hyst_30.0K_20x_01_01
folderid='30.0K_20x_01';
mainFolder='E:\phddatabox\MOLastFrancia\20x\region01\Hyst_30.0K_20x_01_01\';
meas=load('E:\phddatabox\MOLastFrancia\20x\region01\Hyst_30.0K_20x_01_01\meas_disks\d01_50um_Coordinates_Hyst_30.0K_20x_01.dat');
bkg=load('E:\phddatabox\MOLastFrancia\20x\region01\Hyst_30.0K_20x_01_01\meas_disks\d01_50um_Hyst_30.0K_20x_01_bkgId_2.dat');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%++++++++++++++++++++
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%select folder 
%01: Increasing field
if(loopId == 1)
         subFolder='01\'
end
%02: Decreasing field
if(loopId == 2)
         subFolder='02\'
end
s = [mainFolder subFolder] 
cd (s)
%***************************************
%load disk meas values
%measvector(1): diskID
%measvector(2):x0
%measvector(3):y0
%measvector(4):x1
%measvector(5):y1
%measvector(6):param_n_x % ej 0.3
%measvector(7):param_n_y % ej 0.3
%measvector(8):param_m_x defines length profiles in x % ej 0.75
%measvector(9):param_m_y defines length profiles in y 
%***************************************
k_final=length(meas);
measvector=zeros(k_final,1);
for k=1:k_final
    measvector(k)=meas(k,1);
    %measvector(k)
end

%load background
%bkgvector=zeros(4,1);
%bkg_vector(1) = x_bkg;
%bkg_vector(2) = y_bkg;
%bkg_vector(3) = d_bkg_x;
%bkg_vector(4) = d_bkg_y;
%***************************************
k_final=length(bkg);
bkg_vector=zeros(k_final,1);
for k=1:k_final
    bkg_vector(k)=bkg(k,1);
    bkg(k,1)
end
%***************************************
%Assign to variables
diskid =  measvector(1)
%Disk Load
disk_bounds=zeros(4,1);
disk_bounds =[measvector(2), measvector(3), measvector(4), measvector(5)]
param_n_x = measvector(6)
param_n_y = measvector(7)
param_m_x = measvector(8)
param_m_y = measvector(9)
%Background Load
bkg_bounds = zeros(2,1);
bkg_bounds = [bkg_vector(1), bkg_vector(2);]
dbkg_x = bkg_vector(3);
dbkg_y = bkg_vector(4);
%Disk Parametrization
d_disk = zeros(2,1);
d_disk = [disk_bounds(3)-disk_bounds(1),disk_bounds(4)-disk_bounds(2)]
area_disk = d_disk(1)*d_disk(2)
disk_size_av = (d_disk(1)+d_disk(2))*0.5
xcm=(disk_bounds(1)+d_disk(1)/2.0)
ycm=(disk_bounds(2)+d_disk(2)/2.0)
%Profile length
ex_profile= d_disk(1)*param_m_x/2.0
ey_profile=d_disk(2)*param_m_y/2.0
bbox_profile = zeros(4,1);
bbox_profile = [xcm-ex_profile, ycm-ey_profile,	xcm+ex_profile, ycm+ey_profile]
%Magnetic material selection
alpha = d_disk(1)*param_n_x*0.5
beta = d_disk(2)*param_n_y*0.5

%Reassign to old calculation program (From France)
%rectangle with magnetic material
x0_magMaterial = disk_bounds(1)+alpha %former e variable
y0_magMaterial = disk_bounds(2)+beta%former f variable
x_magMaterial = disk_bounds(1)+d_disk(1)-alpha %former g variable
y_magMaterial = disk_bounds(2)+d_disk(2)-beta %former h variable
%rectangle with profile length
x0_profile=bbox_profile(1) %former a variable
y0_profile=bbox_profile(2) %former b variable
x_profile=bbox_profile(3) %former c variable
y_profile=bbox_profile(4) %former d variable
%background rectangle 
xb = bkg_bounds(1)
yb= bkg_bounds(2)
dxb= dbkg_x
dyb= dbkg_y
%***************************************
%Load images for calculation
%***************************************
ImageSource=dir(fileformat);
numberOfFileds=length(ImageSource); %default

if (flag_loop_pick_pics ~= 0)
    numberOfFileds= flag_loop_pick_pics;
end

%Variable inizialization
noir= 0;


mhor = zeros(numberOfFileds,1+x_profile-x0_profile); %dim: field x horizontal lenght + 1
%rows = numberOfFileds (y coordinate), columns = x coordinates
mver = zeros(numberOfFileds,1+y_profile-y0_profile); %dim: field x horizontal lenght + 1
numberOfFileds
Intenout = zeros(numberOfFileds,1); 
%dim: field x 1

Happ = zeros(numberOfFileds,1);
%dim: field x 1

%Matrices z, zLong, zPerp, zBackground
zBackground = zeros(yb:yb+dyb,xb:xb+dxb);
filenamei  = ImageSource(1).name; %string

z = zeros(size(imread(filenamei),1),size(imread(filenamei),2));

zLong = zeros(y0_magMaterial:y_magMaterial,x0_profile:x_profile); %longitudinal, DIM: material_Y_lenghtxImg_lengh 
%rows = y coordinate -> average over magnetic material!! , columns = x coordinates -> profile!!
zPerp = zeros(y0_profile:y_profile,x0_magMaterial:x_magMaterial);
%rows = y coordinate -> profile!!, columns = x coordinates -> average over magnetic
%material!!



%LOOP get intensity values from images
for i=1: numberOfFileds

    filenamei  = ImageSource(i).name;
    %open image 
     
    z=imread(filenamei);
    %get the gaySacale Data in z matrix from image i
    
    %Get field value from Filename
    field=filenamei(5:length(filenamei) -6);
    field(regexp(field,',')) = '.';
    Happ(i)=str2double(field);
    
    %Background load to check then calibration curve points
    zBackground=z(yb:yb+dyb,xb:xb+dxb);
    Intenout(i)=mean2(zBackground); 
    
    %Load profiles in matrices
    zLong=z(y0_magMaterial:y_magMaterial,x0_profile:x_profile);
    %rows = y coordinate -> average over magnetic material!! , columns = x coordinates -> profile!!
    zPerp=z(y0_profile:y_profile,x0_magMaterial:x_magMaterial); 
    %rows = y coordinate -> profile!!, columns = x coordinates -> average over magnetic material!!

    %Define min intensity



    %Horizontal profile for each field. 
    %DIM: field x horizontal lenght + 1
    %ACA Habria que meterle la funcion x2/a2 + y2/b2 =1
    mhor(i,:)=sum(zLong)/(y_magMaterial-y0_magMaterial+1);
    %example sum() 
    %M = 
     %8    1    6
     %3    5    7
     %4    9    2
     %sum(M) =
     %15    15    15
     %     Transposing
     %sum(M') = 
    %     15    15    15
    
    %Vertical profile for each field. DIM: field x verticallenght + 1
    mver(i,:)=sum(zPerp.')/(x_magMaterial-x0_magMaterial+1);
    
    %Display profiles & resulting image selectrion from bounds
    if (flag_show_profiles)
   
        noir=min(min(zLong));
        %Add band 4px with min values along material bound selection 
        %Just to show image below not for calculations 
        %NOT USED IN CALCULATIONS
        z(y0_magMaterial-2:y0_magMaterial+2,:) = noir; 
        z(:,x0_magMaterial-2:x0_magMaterial+2) = noir;
        z(y_magMaterial-2:y_magMaterial+2,:) = noir;
        z(:,x_magMaterial-2:x_magMaterial+2) = noir;
        
        figure(1);
        subplot(4,1,1); imshow(z(y0_profile:y_profile,x0_profile:x_profile),[]);
        title('data');
        subplot(4,1,2); plot(mhor(i,:));
        subplot(4,1,3); plot(mver(i,:));
        title(filenamei);
    if (strcmp(fileformat,'*.tif'))
        subplot(4,1,4); imshow(z(1050:1024,1:450));
    end
    end
    
end

out1='../'
subFolder(regexp(subFolder,'\')) = '';
%***************************************
%Horizontal output file
%***************************************
result = [ 0 Happ' ; [x0_profile:x_profile;  mhor]' ];
% first row : 0 Field values x mhor 
%operator ' -> transpose matrix
[tmp,idx]= sort(result(1,:));
result = result(:,idx); 
%Verified! well arranged! element 1 starts from higher fields 
out2='.dat';
%filename format
out = [out1 folderid '_d' num2str(diskid) '_intensity_h_' num2str(subFolder) out2]
dlmwrite(out, result, 'delimiter', '\t', 'newline', 'pc' );

%***************************************
%Horizontal output file
%***************************************
result = [ 0 Happ'; [y0_profile:y_profile; mver]' ];
[tmp,idx]=sort( result(1,:));
%Verified! well arranged! element 1 starts from higher fields 
result = result(:,idx);
%filename format
out = [out1 folderid '_d' num2str(diskid) '_intensity_v_' num2str(subFolder) out2] ;
dlmwrite(out, result, 'delimiter', '\t', 'newline', 'pc' );


