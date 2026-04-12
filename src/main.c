#include <stdio.h>
#include <stdint.h>

#define N 1000
int16_t buff[N];

int main()
{
    FILE *in = popen("ffmpeg -i /Users/akashfokane/Code/audioStripper/sample.wav -f s16le -ac 1 pipe:1", "r");

    FILE *csv = fopen("sample.csv", "w");

    int16_t sample;
    while (fread(&sample, sizeof(int16_t), 1, in) == 1)
    {
        fprintf(csv, "%d\n", sample);
    }

    pclose(in);
    fclose(csv);
}