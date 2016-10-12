%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Choose Img
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

cd E:\phddatabox\MOLastFrancia\20x\region01\Hyst_08.0K_20x_01_01\meas_disks\;
sourceImg = '023; 242,08G-.jpg'

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
I=imread(sourceImg);

flag_saveImgAsDat = false

if (flag_saveImgAsDat)
    [sx,sy]=size(I)
    fp_b=fopen('E:\phddatabox\MOLastFrancia\20x\region01\'+sourceImg+'.dat','w');
    for i=1:sx
        for j=1:sy
            fprintf(fp_b,'%d\t',I(i,j));
        end
        fprintf(fp_b,'\n');
    end
end

imshow(I);