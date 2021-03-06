// ----------------------------------------------------------------------
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License
// ----------------------------------------------------------------------

#define CATCH_CONFIG_MAIN
#include "catch.hpp"

#include "../ForecastingPivotFeaturizer.h"
#include "../TestHelpers.h"

namespace NS = Microsoft::Featurizer;

#if (defined __clang__)
#   pragma clang diagnostic push
#   pragma clang diagnostic ignored "-Wfloat-equal"
#endif

TEST_CASE("Invalid execute argument") {
    using InputType                         = std::double_t;
    using NullableType                      = NS::Traits<InputType>::nullable_type;
    using TransformedType                   = std::vector<InputType>;
    using MatrixType                        = Eigen::Map<NS::RowMajMatrix<NullableType>>;
    using Matrixes                          = std::vector<MatrixType>;
    using ForecastingPivotTransformer       = NS::Featurizers::ForecastingPivotTransformer<std::tuple<Matrixes::iterator, Matrixes::iterator>>;

    NullableType matrix_data[12]{0};

    MatrixType matrix1(matrix_data, 3, 4);
    MatrixType matrix2(matrix_data, 4, 3);

    std::vector<TransformedType> ret;
    auto const              callback(
        [&ret](TransformedType value) {
            ret.emplace_back(value);
        }
    );

    std::vector<MatrixType>                 matrixes{ std::move(matrix1), std::move(matrix2) };

    CHECK_THROWS_WITH(ForecastingPivotTransformer().execute(std::make_tuple(matrixes.begin(), matrixes.begin()), callback), "There's no input matrix passed in!");
    CHECK_THROWS_WITH(ForecastingPivotTransformer().execute(std::make_tuple(matrixes.begin(), matrixes.end()), callback), "All input matrixes should have the same number of columns!");
}

TEST_CASE("One matrix of double") {
    using InputType                         = std::double_t;
    using NullableType                      = NS::Traits<InputType>::nullable_type;
    using TransformedType                   = std::vector<InputType>;
    using MatrixType                        = Eigen::Map<NS::RowMajMatrix<NullableType>>;
    using Matrixes                          = std::vector<MatrixType>;
    using ForecastingPivotTransformer       = NS::Featurizers::ForecastingPivotTransformer<std::tuple<Matrixes::iterator, Matrixes::iterator>>;

    // 1    4    6 null
    // 2    5 null null
    // 3 null null    7

    NullableType matrixData[]{1, 4, 6, NS::Traits<NullableType>::CreateNullValue(),
                              2, 5, NS::Traits<NullableType>::CreateNullValue(), NS::Traits<NullableType>::CreateNullValue(),
                              3, NS::Traits<NullableType>::CreateNullValue(), NS::Traits<NullableType>::CreateNullValue(), 7};

    MatrixType                                  matrix(matrixData, 3, 4);

    std::vector<TransformedType> ret;
    auto const              callback(
        [&ret](TransformedType value) {
            ret.emplace_back(value);
        }
    );

    Matrixes                                matrixes{ std::move(matrix) };

    ForecastingPivotTransformer().execute(std::make_tuple(matrixes.begin(), matrixes.end()), callback);

    CHECK(ret.size()    == 1);
    CHECK(ret[0].size() == 3);
    CHECK(ret[0][0]     == 1);
    CHECK(ret[0][1]     == 2);
    CHECK(ret[0][2]     == 3);
}

TEST_CASE("Two matrixes of string") {
    using InputType                         = std::string;
    using NullableType                      = NS::Traits<InputType>::nullable_type;
    using TransformedType                   = std::vector<InputType>;
    using MatrixType                        = Eigen::Map<NS::RowMajMatrix<NullableType>>;
    using Matrixes                          = std::vector<MatrixType>;
    using ForecastingPivotTransformer       = NS::Featurizers::ForecastingPivotTransformer<std::tuple<Matrixes::iterator, Matrixes::iterator>>;
    // matrix1
    // "one"   "six" "three"  "nine"
    // "two"  "four"  "five" "eight"
    //  null    null "seven"   "ten"

    NullableType matrix1Data[]{"one", "six", "three", "nine",
                               "two", "four", "five", "eight",
                               NS::Traits<NullableType>::CreateNullValue(), NS::Traits<NullableType>::CreateNullValue(), "seven", "ten"};

    // matrix2
    //    "1"  null    "5"      "6"
    //    "2"  null    "3"      "4"

    NullableType matrix2Data[]{"1", NS::Traits<NullableType>::CreateNullValue(), "5", "6",
                               "2", NS::Traits<NullableType>::CreateNullValue(), "3", "4"};

    MatrixType                                  matrix1(matrix1Data, 3, 4);
    MatrixType                                  matrix2(matrix2Data, 2, 4);

    std::vector<TransformedType> ret;
    auto const              callback(
        [&ret](TransformedType value) {
            ret.emplace_back(value);
        }
    );

    Matrixes                                matrixes{ std::move(matrix1), std::move(matrix2) };

    ForecastingPivotTransformer().execute(std::make_tuple(matrixes.begin(), matrixes.end()), callback);

    CHECK(ret.size()    == 2);
    CHECK(ret[0].size() == 5);
    CHECK(ret[1].size() == 5);

    CHECK(ret[0][0]     == "three");
    CHECK(ret[0][1]     == "five");
    CHECK(ret[0][2]     == "seven");
    CHECK(ret[0][3]     == "5");
    CHECK(ret[0][4]     == "3");

    CHECK(ret[1][0]     == "nine");
    CHECK(ret[1][1]     == "eight");
    CHECK(ret[1][2]     == "ten");
    CHECK(ret[1][3]     == "6");
    CHECK(ret[1][4]     == "4");
}

TEST_CASE("Transformer serialization") {
    using InputType                         = std::string;
    using NullableType                      = NS::Traits<InputType>::nullable_type;
    using MatrixType                        = Eigen::Map<NS::RowMajMatrix<NullableType>>;
    using Matrixes                          = std::vector<MatrixType>;
    using ForecastingPivotTransformer       = NS::Featurizers::ForecastingPivotTransformer<std::tuple<Matrixes::iterator, Matrixes::iterator>>;

    ForecastingPivotTransformer             original;
    NS::Archive                             out;

    original.save(out);

    NS::Archive                             in(out.commit());
    ForecastingPivotTransformer             other(in);

    CHECK(other == original);
}

TEST_CASE("Serialization Version Error") {
    using InputType                         = std::string;
    using NullableType                      = NS::Traits<InputType>::nullable_type;
    using MatrixType                        = Eigen::Map<NS::RowMajMatrix<NullableType>>;
    using Matrixes                          = std::vector<MatrixType>;
    using ForecastingPivotTransformer       = NS::Featurizers::ForecastingPivotTransformer<std::tuple<Matrixes::iterator, Matrixes::iterator>>;

    NS::Archive                             out;

    out.serialize(static_cast<std::uint16_t>(2));
    out.serialize(static_cast<std::uint16_t>(0));

    NS::Archive                             in(out.commit());

    CHECK_THROWS_WITH(
        ForecastingPivotTransformer(in),
        Catch::Contains("Unsupported archive version")
    );
}

#if (defined __clang__)
#   pragma clang diagnostic pop
#endif
