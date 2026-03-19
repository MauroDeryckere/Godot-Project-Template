#include "godot/MyNode.hpp"
#include "engine/Time.hpp"

#include <godot_cpp/core/class_db.hpp>
#include <godot_cpp/variant/utility_functions.hpp>

using namespace godot;

void MyNode::_process(double delta)
{
    engine::Time::Update(delta);

    UtilityFunctions::print(engine::Time::GetDelta());
}

void MyNode::_bind_methods()
{
    // can be empty for now
}
