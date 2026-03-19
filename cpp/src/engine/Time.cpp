#include "engine/Time.hpp"

namespace engine
{
    float Time::s_Delta = 0.0f;

    void Time::Update(double delta)
    {
        s_Delta = static_cast<float>(delta);
    }

    float Time::GetDelta()
    {
        return s_Delta;
    }
}