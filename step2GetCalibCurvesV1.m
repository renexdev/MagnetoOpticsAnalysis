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
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
close all;
clear all;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Info given by user
%Hyst_30.0K_20x_01_01
diskId = 'd01' %50um
temperaturaId = '30.0K'
bkg_id=02;
basePath = 'E:\phddatabox\MOLastFrancia\20x\region01\Hyst_30.0K_20x_01_01\'
fileBkg = 'meas_disks\d01_50um_Coordinates_Hyst_30.0K_20x_01.dat'
%tests
fileBkg = 'meas_disks\d01_50um_Hyst_30.0K_20x_01_bkgId_2.dat'



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
fileBkgPath = [basePath fileBkg]
bkg=load(fileBkgPath);
k_final=4;
bkg_vectorFromFile=zeros(k_final,1);
for k=1:k_final
    bkg_vectorFromFile(k)=bkg(k,1);
    bkg(k,1)
end
x_bkg=bkg_vectorFromFile(1);
y_bkg=bkg_vectorFromFile(2);
d_bkg_x=bkg_vectorFromFile(3);
d_bkg_y=bkg_vectorFromFile(4);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%where to save calibration curve
outputFile=basePath;
inputFile=basePath;
fileformat='*.tif'
fix1='_Hyst_'
fix2 = '_20x_01_';
var1 = 'bkgId_'
var2 = 'IvsH_'
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%out = [outputFile diskId fix1 temperaturaId fix2 var1 num2str(bkg_id) '.dat']
%bkgid = fopen(out,'w');
out = [outputFile diskId fix1 temperaturaId fix2 var2 var1 num2str(bkg_id) '.dat']
fitorginfile=fopen(out,'w');
%%Ascending descending field
out = [outputFile diskId fix1 temperaturaId fix2 var2 var1 num2str(bkg_id) '_01.dat']
fitorginfileIncreasingField=fopen(out,'w');
out = [outputFile diskId fix1 temperaturaId fix2 var2 var1 num2str(bkg_id) '_02.dat']
fitorginfileDecreasingField=fopen(out,'w');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Save bkg conditions
%bkgvector=zeros(4,1);
%bkg_vector(1) = x_bkg;
%bkg_vector(2) = y_bkg;
%bkg_vector(3) = d_bkg_x;
%bkg_vector(4) = d_bkg_y;
%for k=1:4
%    bkg_vector(k)
%    fprintf(bkgid,'%d\n', bkg_vector(k));
%end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
subFolder='01\'
%subFolder='01Test\'
s = [inputFile subFolder] 
cd (s)
ImageSource = dir(fileformat); %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
numberOfFileds = length(ImageSource);

IntensityOut = ones(numberOfFileds,1);
Happ = ones(numberOfFileds,1);
%rows x columns
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for i=1:length(ImageSource)
        filename  = ImageSource(i).name;
        %open image & get the gaySacale Data in z matrix
        
        z = imread(filename); 
        %Funcion que lleva 12 bits a 8 bits de python
        %z = im2uint8(z);
        %Get field from File
        %field=filename(4:length(filename) -6); %cambio
        field=filename(5:length(filename) -6)
        field(regexp(field,',')) = '.'
        Happ(i)=str2double(field);
        
        %Get selected background from z matrix
        zout=z(y_bkg:y_bkg+d_bkg_y,x_bkg:x_bkg+d_bkg_x);
        %punto x280,y81 en python
        %zout1=z(82,281)
        %punto x0,y0 en python
        %zout1=z(1,1)
        

        %rows = y coordinate, columns = x coordinates
        %i
        %zout
        IntensityOut(i) = mean2(zout); %vector containing data of luminous intensity (background)
        
        %ex. mean2 fnc:
        %A = [[1,2],[3, 4]]
        %mean2(A) = 2.5
        fprintf(fitorginfile,'%.2f\t%.2f\n', IntensityOut(i),Happ(i));
        fprintf(fitorginfileIncreasingField,'%.2f\t%.2f\n', IntensityOut(i),Happ(i));
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
subFolder='02\'
%subFolder='02Test\'
s = [inputFile subFolder] 
cd (s)
ImageSource=dir(fileformat); %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
numberOfFileds=length(ImageSource);
IntensityOut=ones(numberOfFileds,1);
Happ=ones(numberOfFileds,1);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for i=1:length(ImageSource)
        filename  = ImageSource(i).name;
        z=imread(filename); 
        %Funcion que lleva 12 bits a 8 bits de python
        %z = im2uint8(z);
        %field=filename(4:length(filename) -6); %cambio
        field=filename(5:length(filename) -6)
        field(regexp(field,',')) = '.'
        Happ(i)=str2double(field);
        zout=z(y_bkg:y_bkg+d_bkg_y,x_bkg:x_bkg+d_bkg_x);
        %i
        %zout
       %zout1=z(y_bkg,x_bkg);
        %zout1
        IntensityOut(i)=mean2(zout); %vector containing data of luminous intensity (background)
        fprintf(fitorginfile,'%.2f\t%.2f\n', IntensityOut(i),Happ(i));
        fprintf(fitorginfileDecreasingField,'%.2f\t%.2f\n', IntensityOut(i),Happ(i));
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
fclose(fitorginfile);
%fclose(bkgid);
fclose(fitorginfileIncreasingField);
fclose(fitorginfileDecreasingField);
%print bkg coordinates!!! to check
for k=1:k_final
    bkg(k,1)
end
       

        
       