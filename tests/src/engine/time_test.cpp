#include <catch2/catch_test_macros.hpp>
#include <catch2/matchers/catch_matchers_floating_point.hpp>

#include "engine/Time.hpp"

TEST_CASE("Time tracks delta", "[engine][time]")
{
	engine::Time::Update(0.016);
	REQUIRE_THAT(engine::Time::GetDelta(), Catch::Matchers::WithinAbs(0.016f, 0.0001f));

	engine::Time::Update(0.033);
	REQUIRE_THAT(engine::Time::GetDelta(), Catch::Matchers::WithinAbs(0.033f, 0.0001f));
}

TEST_CASE("Time defaults to zero", "[engine][time]")
{
	engine::Time::Update(0.0);
	REQUIRE(engine::Time::GetDelta() == 0.0f);
}
