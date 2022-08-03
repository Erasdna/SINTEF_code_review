%Vi endrer faktoren alle størrelsene i batteriet ganges med
mult=1:2:35;
tm=zeros(1,length(mult));

for i=1:length(mult)
    tm(i)=Chen2020TimeTest(mult(i));
end

fileID=fopen("battmoTime_SD_notsimple.txt",'w');
%Gange med 30, som er den originale størrelsen, for å få den nye
fprintf(fileID,'%6.2f %6.2f \n',[tm;mult.*30]);
fclose(fileID);