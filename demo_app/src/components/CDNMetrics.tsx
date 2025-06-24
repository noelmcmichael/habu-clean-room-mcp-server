import React, { useState, useEffect } from 'react';
import { 
    TrendingUp, 
    Zap, 
    Globe, 
    BarChart3, 
    Clock,
    Download,
    CheckCircle,
    Activity
} from 'lucide-react';

interface CDNStats {
    total_requests: number;
    cache_hit_ratio: number;
    compression_ratio: number;
    average_response_time: number;
    performance_score: number;
    last_updated: string;
}

interface CDNMetricsProps {
    refreshInterval?: number;
}

const CDNMetrics: React.FC<CDNMetricsProps> = ({ refreshInterval = 30000 }) => {
    const [cdnStats, setCdnStats] = useState<CDNStats | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [lastUpdated, setLastUpdated] = useState<Date>(new Date());

    const fetchCDNStats = async () => {
        try {
            const response = await fetch('/api/cdn-stats');
            if (!response.ok) {
                throw new Error('Failed to fetch CDN stats');
            }
            const data = await response.json();
            setCdnStats(data.cdn_stats);
            setError(null);
            setLastUpdated(new Date());
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Unknown error');
            console.error('CDN stats fetch error:', err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchCDNStats();
        const interval = setInterval(fetchCDNStats, refreshInterval);
        return () => clearInterval(interval);
    }, [refreshInterval]);

    const getPerformanceColor = (score: number): string => {
        if (score >= 80) return 'text-green-400';
        if (score >= 60) return 'text-yellow-400';
        return 'text-red-400';
    };

    const getPerformanceLabel = (score: number): string => {
        if (score >= 80) return 'Excellent';
        if (score >= 60) return 'Good';
        if (score >= 40) return 'Fair';
        return 'Poor';
    };

    if (loading && !cdnStats) {
        return (
            <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
                <div className="flex items-center space-x-2 mb-4">
                    <Globe className="w-5 h-5 text-blue-400" />
                    <h3 className="text-lg font-semibold text-white">CDN Performance</h3>
                </div>
                <div className="animate-pulse">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        {[...Array(4)].map((_, i) => (
                            <div key={i} className="bg-gray-700 h-20 rounded"></div>
                        ))}
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
            <div className="flex items-center justify-between mb-6">
                <div className="flex items-center space-x-2">
                    <Globe className="w-5 h-5 text-blue-400" />
                    <h3 className="text-lg font-semibold text-white">CDN Performance</h3>
                </div>
                <div className="text-sm text-gray-400">
                    Updated: {lastUpdated.toLocaleTimeString()}
                </div>
            </div>

            {error && (
                <div className="bg-red-900/20 border border-red-500/50 rounded-lg p-3 mb-4">
                    <p className="text-red-400 text-sm">Error: {error}</p>
                </div>
            )}

            {cdnStats && (
                <>
                    {/* Performance Score */}
                    <div className="mb-6 p-4 bg-gray-700/50 rounded-lg">
                        <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-2">
                                <Activity className="w-5 h-5 text-purple-400" />
                                <span className="text-white font-medium">Overall Performance</span>
                            </div>
                            <div className="text-right">
                                <div className={`text-2xl font-bold ${getPerformanceColor(cdnStats.performance_score)}`}>
                                    {cdnStats.performance_score}
                                </div>
                                <div className={`text-sm ${getPerformanceColor(cdnStats.performance_score)}`}>
                                    {getPerformanceLabel(cdnStats.performance_score)}
                                </div>
                            </div>
                        </div>
                        <div className="mt-2">
                            <div className="w-full bg-gray-600 rounded-full h-2">
                                <div 
                                    className={`h-2 rounded-full transition-all duration-500 ${
                                        cdnStats.performance_score >= 80 ? 'bg-green-400' :
                                        cdnStats.performance_score >= 60 ? 'bg-yellow-400' : 'bg-red-400'
                                    }`}
                                    style={{ width: `${cdnStats.performance_score}%` }}
                                ></div>
                            </div>
                        </div>
                    </div>

                    {/* Metrics Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                        {/* Total Requests */}
                        <div className="bg-gray-700/50 rounded-lg p-4">
                            <div className="flex items-center space-x-2 mb-2">
                                <BarChart3 className="w-4 h-4 text-blue-400" />
                                <span className="text-sm text-gray-300">Total Requests</span>
                            </div>
                            <div className="text-2xl font-bold text-white">
                                {cdnStats.total_requests.toLocaleString()}
                            </div>
                        </div>

                        {/* Cache Hit Ratio */}
                        <div className="bg-gray-700/50 rounded-lg p-4">
                            <div className="flex items-center space-x-2 mb-2">
                                <CheckCircle className="w-4 h-4 text-green-400" />
                                <span className="text-sm text-gray-300">Cache Hit Ratio</span>
                            </div>
                            <div className="text-2xl font-bold text-green-400">
                                {cdnStats.cache_hit_ratio}%
                            </div>
                        </div>

                        {/* Compression Ratio */}
                        <div className="bg-gray-700/50 rounded-lg p-4">
                            <div className="flex items-center space-x-2 mb-2">
                                <Download className="w-4 h-4 text-purple-400" />
                                <span className="text-sm text-gray-300">Compression</span>
                            </div>
                            <div className="text-2xl font-bold text-purple-400">
                                {cdnStats.compression_ratio}%
                            </div>
                        </div>

                        {/* Average Response Time */}
                        <div className="bg-gray-700/50 rounded-lg p-4">
                            <div className="flex items-center space-x-2 mb-2">
                                <Clock className="w-4 h-4 text-yellow-400" />
                                <span className="text-sm text-gray-300">Avg Response</span>
                            </div>
                            <div className="text-2xl font-bold text-yellow-400">
                                {cdnStats.average_response_time}ms
                            </div>
                        </div>
                    </div>

                    {/* Performance Insights */}
                    <div className="mt-6 p-4 bg-gray-700/30 rounded-lg">
                        <h4 className="text-sm font-medium text-white mb-3">Performance Insights</h4>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                            <div className="flex items-center space-x-2">
                                <Zap className="w-4 h-4 text-blue-400" />
                                <span className="text-gray-300">
                                    CDN Optimization: <span className="text-white">Active</span>
                                </span>
                            </div>
                            <div className="flex items-center space-x-2">
                                <TrendingUp className="w-4 h-4 text-green-400" />
                                <span className="text-gray-300">
                                    Compression: <span className="text-white">Enabled</span>
                                </span>
                            </div>
                            <div className="flex items-center space-x-2">
                                <Globe className="w-4 h-4 text-purple-400" />
                                <span className="text-gray-300">
                                    Edge Caching: <span className="text-white">Ready</span>
                                </span>
                            </div>
                        </div>
                    </div>
                </>
            )}
        </div>
    );
};

export default CDNMetrics;