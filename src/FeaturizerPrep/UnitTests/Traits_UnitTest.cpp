// ----------------------------------------------------------------------
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License
// ----------------------------------------------------------------------
#define CATCH_CONFIG_MAIN
#include "catch.hpp"

#include "../Traits.h"
#include "../Archive.h"

#include <type_traits>

using namespace Microsoft::Featurizer;

// Floating point values
static_assert(std::is_same<Traits<float>::nullable_type, float>::value, "Incorrect nullable type for float");
static_assert(std::is_same<Traits<double>::nullable_type, double>::value, "Incorrect nullable type for double");

// Int values
static_assert(std::is_same<Traits<std::int8_t>::nullable_type, nonstd::optional<std::int8_t>>::value, "Incorrect nullable type for std::int8_t");
static_assert(std::is_same<Traits<std::int16_t>::nullable_type, nonstd::optional<std::int16_t>>::value, "Incorrect nullable type for std::int16_t");
static_assert(std::is_same<Traits<std::int32_t>::nullable_type, nonstd::optional<std::int32_t>>::value, "Incorrect nullable type for std::int32_t");
static_assert(std::is_same<Traits<std::int64_t>::nullable_type, nonstd::optional<std::int64_t>>::value, "Incorrect nullable type for std::int64_t");
static_assert(std::is_same<Traits<std::uint8_t>::nullable_type, nonstd::optional<std::uint8_t>>::value, "Incorrect nullable type for std::uint8_t");
static_assert(std::is_same<Traits<std::uint16_t>::nullable_type, nonstd::optional<std::uint16_t>>::value, "Incorrect nullable type for std::uint16_t");
static_assert(std::is_same<Traits<std::uint32_t>::nullable_type, nonstd::optional<std::uint32_t>>::value, "Incorrect nullable type for std::uint32_t");
static_assert(std::is_same<Traits<std::uint64_t>::nullable_type, nonstd::optional<std::uint64_t>>::value, "Incorrect nullable type for std::uint64_t");

// Others
static_assert(std::is_same<Traits<std::string>::nullable_type, nonstd::optional<std::string>>::value, "Incorrect nullable type for std::string");
static_assert(std::is_same<Traits<std::array<char, 4>>::nullable_type, nonstd::optional<std::array<char, 4>>>::value, "Incorrect nullable type for std::array");
static_assert(std::is_same<Traits<bool>::nullable_type, nonstd::optional<bool>>::value, "Incorrect nullable type for std::string");
static_assert(std::is_same<Traits<std::map<int,int>>::nullable_type, nonstd::optional<std::map<int,int>>>::value, "Incorrect nullable type for std::string");
static_assert(std::is_same<Traits<std::vector<int>>::nullable_type, nonstd::optional<std::vector<int>>>::value, "Incorrect nullable type for std::string");
static_assert(std::is_same<Traits<nonstd::optional<int>>::nullable_type, nonstd::optional<int>>::value, "Incorrect nullable type for std::string");
static_assert(std::is_same<Traits<std::tuple<int>>::nullable_type, nonstd::optional<std::tuple<int>>>::value, "Incorrect nullable type for std::string");

TEST_CASE("Transformer_Nullable") {
    nonstd::optional<std::int8_t> arg_null;
	std::float_t arg_f_ini = std::numeric_limits<std::float_t>::quiet_NaN();
	std::double_t arg_d_ini = std::numeric_limits<std::double_t>::quiet_NaN();

	nonstd::optional<std::int64_t> arg_64(-7799);
    std::float_t arg_f = 123;
    std::double_t arg_d = 123.45;

    CHECK(Traits<nonstd::optional<std::int8_t>>::ToString(arg_null) == "NULL");
	CHECK(Traits<std::float_t>::ToString(Traits<std::float_t>::GetNullableValue(arg_f)) == "123.000000");
	CHECK(Traits<nonstd::optional<std::int64_t>>::GetNullableValue(arg_64) == -7799);
	CHECK(Traits<std::double_t>::ToString(Traits<std::double_t>::GetNullableValue(arg_d)) == "123.450000");

	CHECK_THROWS_WITH(Traits<nonstd::optional<std::int8_t>>::GetNullableValue(arg_null)
				, Catch::Contains("GetNullableValue attempt on Optional type null."));
	CHECK_THROWS_WITH(Traits<float_t>::GetNullableValue(arg_f_ini)
				, Catch::Contains("GetNullableValue attempt on float_t null."));
	CHECK_THROWS_WITH(Traits<double_t>::GetNullableValue(arg_d_ini)
				, Catch::Contains("GetNullableValue attempt on double_t null"));
}

TEST_CASE("Transformer_Binary") {
    bool arg_false = false;
    bool arg_true = true;
    CHECK(Traits<bool>::ToString(arg_false) == "False");
    CHECK(Traits<bool>::ToString(arg_true) == "True");
}

TEST_CASE("Transformer_Strings") {
    std::string arg_s = "isstring";
    CHECK(Traits<std::string>::ToString(arg_s) == "isstring");
}

TEST_CASE("Transformer_Integers") {
    std::int8_t arg_8 = 20;
    std::int16_t arg_16 = -250;
    std::int32_t arg_32 = 480;
    std::int64_t arg_64 = -7799;

    std::uint8_t arg_u8 = 20;
    std::uint16_t arg_u16 = 250;
    std::uint32_t arg_u32 = 480;
    std::uint64_t arg_u64 = 7799;

    CHECK(Traits<std::int8_t>::ToString(arg_8) == "20");
    CHECK(Traits<std::int16_t>::ToString(arg_16) == "-250");
    CHECK(Traits<std::int32_t>::ToString(arg_32) == "480");
    CHECK(Traits<std::int64_t>::ToString(arg_64) == "-7799");

    CHECK(Traits<std::uint8_t>::ToString(arg_u8) == "20");
    CHECK(Traits<std::uint16_t>::ToString(arg_u16) == "250");
    CHECK(Traits<std::uint32_t>::ToString(arg_u32) == "480");
    CHECK(Traits<std::uint64_t>::ToString(arg_u64) == "7799");
}

TEST_CASE("Transformer_Numbers") {
	std::float_t arg_f_ini = std::numeric_limits<std::float_t>::quiet_NaN();
	std::double_t arg_d_ini = std::numeric_limits<std::double_t>::quiet_NaN();
    std::float_t arg_f = 123;
    std::double_t arg_d1 = 123.45;
    std::double_t arg_d2 = 135453984983490.5473;

    CHECK(Traits<std::float_t>::ToString(arg_f_ini) == "NaN");
    CHECK(Traits<std::double_t>::ToString(arg_d_ini) == "NaN");
    CHECK(Traits<std::float_t>::ToString(arg_f) == "123.000000");
    CHECK(Traits<std::double_t>::ToString(arg_d1) == "123.450000");
    CHECK(Traits<std::double_t>::ToString(arg_d2) == "135453984983490.546875");
}

TEST_CASE("Transformer_Arrays") {
    std::array<std::double_t, 4> arr{ 1.3,2,-306.2,0.04 };
    std::string arr_s{ "[1.300000,2.000000,-306.200000,0.040000]" };
    CHECK(Traits<std::array<std::double_t, 4>>::ToString(arr) == arr_s);

    //array<optional>
    nonstd::optional<std::double_t> arg_null;
	std::array<nonstd::optional<std::double_t>, 3> arr_hasnull{1.5,arg_null,-47.1};
	std::string arr_hasnull_s{"[1.500000,NULL,-47.100000]"};
	CHECK(Traits<std::array<nonstd::optional<std::double_t>, 3>>::ToString(arr_hasnull) == arr_hasnull_s);

    //vectors in arrays
    std::vector<std::double_t> vect{ 1.03, -20.1, 305.8 };
    std::array< std::vector<std::double_t>, 2> vecinarr{vect, vect};
    std::string vecinarr_res = Traits<std::array< std::vector<std::double_t>, 2>>::ToString(vecinarr);
    std::string vecinarr_s{"[[1.030000,-20.100000,305.800000],[1.030000,-20.100000,305.800000]]"};
    CHECK(vecinarr_res == vecinarr_s);

}

TEST_CASE("Transformer_Vectors") {
    std::vector<std::double_t> vect{ 1.03, -20.1, 305.8 };
    std::string vect_s{ "[1.030000,-20.100000,305.800000]" };
	CHECK(Traits<std::vector<std::double_t>>::ToString(vect) == vect_s);

	//vector<optional>
	nonstd::optional<std::int8_t> arg_null;
	std::vector<nonstd::optional<std::int8_t>> vect_hasnull{static_cast<std::int8_t>(1), static_cast<std::int8_t>(2), arg_null, static_cast<std::int8_t>(4)};
	std::string vect_hasnull_s{"[1,2,NULL,4]"};
	CHECK(Traits<std::vector<nonstd::optional<std::int8_t>>>::ToString(vect_hasnull) == vect_hasnull_s);

	//vectors in vectors
	std::vector<std::int16_t> Bvect{2, 3, 7, -9};
    std::vector<std::vector<std::int16_t>> Rvect(2, Bvect);
    std::vector<std::vector<std::vector<std::int16_t>>> R2vect(2, Rvect);
    std::string Rvect_res = Traits<std::vector<std::vector<std::int16_t>>>::ToString(Rvect);
    std::string R2vect_res = Traits<std::vector<std::vector<std::vector<std::int16_t>>>>::ToString(R2vect);
    std::string Rvect_s{ "[[2,3,7,-9],[2,3,7,-9]]" };
    std::string R2vect_s{ "[[[2,3,7,-9],[2,3,7,-9]],[[2,3,7,-9],[2,3,7,-9]]]" };
    CHECK( Rvect_res == Rvect_s);
    CHECK( R2vect_res == R2vect_s);

    //arrays in vectors
    std::array<std::double_t, 3> arrinvec{ 8.8,0.02,3643.7 };
    std::vector<std::array<std::double_t, 3>> vecwitharr;
    vecwitharr.push_back(arrinvec);
    std::string vecwitharr_s{"[[8.800000,0.020000,3643.700000]]"};
    std::string vecwitharr_res = Traits<std::vector<std::array<std::double_t, 3>>>::ToString(vecwitharr);
    CHECK(vecwitharr_res == vecwitharr_s);
}

TEST_CASE("Transformer_Maps") {
    std::map<std::int16_t, std::double_t> m;
    m.insert(std::pair<std::int16_t, std::double_t>(static_cast<std::int16_t>(5), 35.8));
    m.insert(std::pair<std::int16_t, std::double_t>(static_cast<std::int16_t>(93), 0.147));
    std::string map_res = Traits<std::map<std::int16_t, std::double_t>>::ToString(m);
    std::string map_s{ "{5:35.800000,93:0.147000}" };
	CHECK(map_res == map_s);
}

TEST_CASE("Transformer_Tuples") {
    std::tuple<int, std::string, double> tu(42, "hi", -3.14);
    std::string tu_res = Traits<std::tuple<int, std::string, double>>::ToString(tu);
    std::string tu_s{"(42,hi,-3.140000)"};
    CHECK(tu_res == tu_s);
}

#if (defined __clang__)
#   pragma clang diagnostic push
#   pragma clang diagnostic ignored "-Wfloat-equal"
#endif

template <typename T>
bool SerializationTestImpl(T const &value) {
    Archive                                 out;

    Traits<T>::serialize(out, value);

    Archive                                 in(out.commit());
    T const                                 other(Traits<T>::deserialize(in));

    return in.AtEnd() && other == value;
}

#if (defined __clang__)
#   pragma clang diagnostic pop
#endif

TEST_CASE("Serialization") {
    CHECK(SerializationTestImpl(true));
    CHECK(SerializationTestImpl(static_cast<std::int8_t>(-23)));
    CHECK(SerializationTestImpl(static_cast<std::int16_t>(-23)));
    CHECK(SerializationTestImpl(static_cast<std::int32_t>(-23)));
    CHECK(SerializationTestImpl(static_cast<std::int64_t>(-23)));
    CHECK(SerializationTestImpl(static_cast<std::uint8_t>(23)));
    CHECK(SerializationTestImpl(static_cast<std::uint16_t>(23)));
    CHECK(SerializationTestImpl(static_cast<std::uint32_t>(23)));
    CHECK(SerializationTestImpl(static_cast<std::uint64_t>(23)));
    CHECK(SerializationTestImpl(static_cast<std::double_t>(3.14)));
    CHECK(SerializationTestImpl(static_cast<std::float_t>(-3.14)));

    CHECK(SerializationTestImpl(std::string()));
    CHECK(SerializationTestImpl(std::string("Hello world!")));

    CHECK(SerializationTestImpl(std::array<int, 2>{10, 20}));
    CHECK(SerializationTestImpl(std::array<std::string, 2>{"1", "2"}));

    CHECK(SerializationTestImpl(std::vector<int>()));
    CHECK(SerializationTestImpl(std::vector<int>{1, 2, 3}));
    CHECK(SerializationTestImpl(std::vector<std::string>{"one", "two", "three"}));

    CHECK(SerializationTestImpl(std::map<int, std::string>()));
    CHECK(SerializationTestImpl(std::map<int, std::string>{ {10, "ten"}, {20, "twenty"} }));
    CHECK(SerializationTestImpl(std::map<std::string, int>{ {"ten", 10}, {"twenty", 20} }));

    CHECK(SerializationTestImpl(nonstd::optional<int>()));
    CHECK(SerializationTestImpl(nonstd::optional<int>(23)));
    CHECK(SerializationTestImpl(nonstd::optional<std::string>("foo")));

    CHECK(SerializationTestImpl(std::tuple<std::string, int, bool>("one", 2, true)));
}

template <typename T>
bool TestCreateNullValue(void) {
    return Traits<T>::IsNull(Traits<T>::CreateNullValue());
}

TEST_CASE("CreateNullValue") {
    CHECK(TestCreateNullValue<std::int8_t>());
    CHECK(TestCreateNullValue<std::int16_t>());
    CHECK(TestCreateNullValue<std::int32_t>());
    CHECK(TestCreateNullValue<std::int64_t>());
    CHECK(TestCreateNullValue<std::uint8_t>());
    CHECK(TestCreateNullValue<std::uint16_t>());
    CHECK(TestCreateNullValue<std::uint32_t>());
    CHECK(TestCreateNullValue<std::uint64_t>());
    CHECK(TestCreateNullValue<std::float_t>());
    CHECK(TestCreateNullValue<std::double_t>());
    CHECK(TestCreateNullValue<bool>());
    CHECK(TestCreateNullValue<std::string>());
    CHECK(TestCreateNullValue<std::vector<std::string>>());
    CHECK(TestCreateNullValue<std::map<std::string, std::uint32_t>>());
    CHECK(TestCreateNullValue<nonstd::optional<std::int8_t>>());
}
