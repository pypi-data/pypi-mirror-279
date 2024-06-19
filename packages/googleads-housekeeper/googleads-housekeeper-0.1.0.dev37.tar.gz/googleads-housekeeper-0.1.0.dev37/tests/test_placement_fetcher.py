from __future__ import annotations

import gaarf
import pytest

from googleads_housekeeper.domain.core import task
from googleads_housekeeper.domain.placement_handler import placement_fetcher
from googleads_housekeeper.services import enums

_BASE_PLACEMENT_INFO = [
    'example.com',
    'WEBSITE',
    'example.com',
    '1234',
    'example.com',
]

_BASE_PLACEMENT_INFO_WITH_CUSTOMER_ID = _BASE_PLACEMENT_INFO + [1111]

_BASE_REPORT_COLUMN_NAMES = [
    'placement',
    'placement_type',
    'name',
    'criterion_id',
    'url',
]

_BASE_REPORT_COLUMN_NAMES_WITH_CUSTOMER_ID = _BASE_REPORT_COLUMN_NAMES + [
    'customer_id'
]


class TestPlacementFetcher:

    @pytest.fixture
    def test_client(self, mocker):
        mocker.patch('google.ads.googleads.client.oauth2', return_value=[])
        return gaarf.api_clients.GoogleAdsApiClient()

    @pytest.fixture
    def fetcher(self, test_client):
        return placement_fetcher.PlacementFetcher(
            gaarf.query_executor.AdsReportFetcher(test_client))

    @pytest.fixture
    def placements(self):
        return gaarf.report.GaarfReport(
            results=[
                _BASE_PLACEMENT_INFO_WITH_CUSTOMER_ID +
                [2222, 3331, 2, 20, 0.2],
                _BASE_PLACEMENT_INFO_WITH_CUSTOMER_ID +
                [2222, 3332, 5, 50, 0.5],
                _BASE_PLACEMENT_INFO_WITH_CUSTOMER_ID +
                [2223, 3333, 3, 30, 0.3],
            ],
            column_names=_BASE_REPORT_COLUMN_NAMES_WITH_CUSTOMER_ID +
            ['campaign_id', 'ad_group_id', 'clicks', 'impressions', 'cost'])

    def test_aggregate_placements_returns_same_report_for_ad_group_level_aggregation(
            self, fetcher, placements):

        aggregated_report = fetcher._aggregate_placements(
            placements=placements,
            exclusion_level=enums.ExclusionLevelEnum.AD_GROUP,
            perform_relative_aggregations=False)

        assert aggregated_report == placements

    def test_aggregate_placements_returns_correct_report_for_campaign_level_aggregation(
            self, fetcher, placements):

        expected_report = gaarf.report.GaarfReport(
            results=[
                _BASE_PLACEMENT_INFO_WITH_CUSTOMER_ID + [2222, 7, 70, 0.7],
                _BASE_PLACEMENT_INFO_WITH_CUSTOMER_ID + [2223, 3, 30, 0.3],
            ],
            column_names=_BASE_REPORT_COLUMN_NAMES_WITH_CUSTOMER_ID +
            ['campaign_id', 'clicks', 'impressions', 'cost'])

        aggregated_report = fetcher._aggregate_placements(
            placements=placements,
            exclusion_level=enums.ExclusionLevelEnum.CAMPAIGN,
            perform_relative_aggregations=False)

        assert aggregated_report == expected_report

    def test_aggregate_placements_returns_correct_report_for_account_level_aggregation(
            self, fetcher, placements):

        expected_report = gaarf.report.GaarfReport(
            results=[_BASE_PLACEMENT_INFO_WITH_CUSTOMER_ID + [10, 100, 1.0]],
            column_names=_BASE_REPORT_COLUMN_NAMES_WITH_CUSTOMER_ID +
            ['clicks', 'impressions', 'cost'])

        aggregated_report = fetcher._aggregate_placements(
            placements=placements,
            exclusion_level=enums.ExclusionLevelEnum.ACCOUNT,
            perform_relative_aggregations=False)

        assert aggregated_report == expected_report

    def test_aggregate_placements_with_relative_aggretations_returns_extra_columns_in_report(
            self, fetcher, placements):

        expected_report = gaarf.report.GaarfReport(
            results=[
                _BASE_PLACEMENT_INFO_WITH_CUSTOMER_ID +
                [2222, 7, 70, 0.7, 0.1, 0.1, 10.0],
                _BASE_PLACEMENT_INFO_WITH_CUSTOMER_ID +
                [2223, 3, 30, 0.3, 0.1, 0.1, 10.0],
            ],
            column_names=_BASE_REPORT_COLUMN_NAMES_WITH_CUSTOMER_ID + [
                'campaign_id', 'clicks', 'impressions', 'cost', 'ctr',
                'avg_cpc', 'avg_cpm'
            ])

        aggregated_report = fetcher._aggregate_placements(
            placements=placements,
            exclusion_level=enums.ExclusionLevelEnum.CAMPAIGN,
            perform_relative_aggregations=True)

        assert aggregated_report == expected_report

    def test_join_conversion_split(self, fetcher):
        placements = gaarf.report.GaarfReport(
            results=[
                _BASE_PLACEMENT_INFO_WITH_CUSTOMER_ID +
                [2222, 3331, 2, 20, 0.2],
            ],
            column_names=_BASE_REPORT_COLUMN_NAMES_WITH_CUSTOMER_ID +
            ['campaign_id', 'ad_group_id', 'clicks', 'impressions', 'cost'])
        conversion_split_data = gaarf.report.GaarfReport(
            results=[
                [3331, 'example.com', 'test-conversion', 10, 100],
                [3331, 'example.com', 'test-conversion-2', 10, 100],
            ],
            column_names=[
                'ad_group_id', 'placement', 'conversion_name', 'conversions',
                'all_conversions'
            ])
        expected_report = gaarf.report.GaarfReport(
            results=[
                _BASE_PLACEMENT_INFO_WITH_CUSTOMER_ID +
                [2222, 3331, 2, 20, 0.2, 'test-conversion', 10, 100],
            ],
            column_names=_BASE_REPORT_COLUMN_NAMES_WITH_CUSTOMER_ID + [
                'campaign_id', 'ad_group_id', 'clicks', 'impressions', 'cost',
                'conversion_name', 'conversions_', 'all_conversions_'
            ])
        joined_report = fetcher._join_conversion_split(placements,
                                                       conversion_split_data,
                                                       'test-conversion')
        assert joined_report == expected_report

    def test_aggregate_placements_with_conversion_name_returns_extra_cpa_columns_in_report(
            self, fetcher):

        report = gaarf.report.GaarfReport(
            results=[
                _BASE_PLACEMENT_INFO_WITH_CUSTOMER_ID +
                ['test-conversion', 10, 1, 10],
            ],
            column_names=_BASE_REPORT_COLUMN_NAMES_WITH_CUSTOMER_ID +
            ['conversion_name', 'cost', 'conversions_', 'all_conversions_'])
        expected_report = gaarf.report.GaarfReport(
            results=[
                _BASE_PLACEMENT_INFO +
                ['test-conversion', 1111, 10, 1, 10, 10.0, 1.0],
            ],
            column_names=_BASE_REPORT_COLUMN_NAMES + [
                'conversion_name', 'customer_id', 'cost', 'conversions_',
                'all_conversions_', 'cost_per_conversion_',
                'cost_per_all_conversion_'
            ])

        aggregated_report = fetcher._aggregate_placements(
            placements=report,
            exclusion_level=enums.ExclusionLevelEnum.ACCOUNT,
            perform_relative_aggregations=True)

        assert aggregated_report == expected_report

    def test_placements_without_conversion_name_returns_extra_conversion_split_columns_in_report(
            self, mocker, fetcher):
        mock_report = gaarf.report.GaarfReport(
            results=[
                _BASE_PLACEMENT_INFO + ['12345', 10],
            ],
            column_names=_BASE_REPORT_COLUMN_NAMES +
            ['customer_id', 'cost'])
        mocker.patch(
            ('googleads_housekeeper.domain.placement_handler.placement_fetcher'
             '.PlacementFetcher._get_placement_performance_data'),
            return_value=mock_report)

        mocker.patch(
            ('googleads_housekeeper.domain.placement_handler.placement_fetcher'
             '.PlacementFetcher._get_placement_conversion_split_data'),
            return_value=None)

        fake_task = task.Task(
            name='test',
            customer_ids='12345',
            exclusion_rule=('GOOGLE_ADS_INFO:conversion_name contains a AND '
                            'GOOGLE_ADS_INFO:conversions_ > 0')
        )
        aggregated_report = fetcher.get_placements_for_account(
            account='12345', task_obj=fake_task)

        expected = gaarf.report.GaarfReport(
                results=[
                    _BASE_PLACEMENT_INFO + ['', '12345', 10, 0.0, 0.0, 0.0, 0.0]
                ],
                column_names=_BASE_REPORT_COLUMN_NAMES  + [
                'conversion_name', 'customer_id', 'cost', 'conversions_',
                'all_conversions_', 'cost_per_conversion_', 'cost_per_all_conversion_'
            ])

        assert aggregated_report == expected
