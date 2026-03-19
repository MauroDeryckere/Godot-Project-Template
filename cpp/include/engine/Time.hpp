#pragma once

namespace engine
{
    class Time
    {
    public:
        static void Update(double delta);

        static float GetDelta();

    private:
        static float s_Delta;
    };
}