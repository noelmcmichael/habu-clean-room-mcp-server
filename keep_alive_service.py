#!/usr/bin/env python3
"""
Keep-Alive Service for Render.com Free Tier
Prevents cold starts by pinging services every 10 minutes
"""

import asyncio
import aiohttp
import logging
import os
from datetime import datetime
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KeepAliveService:
    """Service to prevent Render.com cold starts by pinging services regularly."""
    
    def __init__(self):
        self.services = [
            {
                "name": "Frontend",
                "url": "https://habu-demo-frontend-v2.onrender.com",
                "health_path": "/",
                "timeout": 10
            },
            {
                "name": "API Bridge", 
                "url": "https://habu-demo-api-v2.onrender.com",
                "health_path": "/api/health",
                "timeout": 15
            },
            {
                "name": "MCP Server",
                "url": "https://habu-mcp-server-v2.onrender.com", 
                "health_path": "/mcp",
                "timeout": 20
            },
            {
                "name": "Admin App",
                "url": "https://habu-admin-app-v2.onrender.com",
                "health_path": "/",
                "timeout": 10
            }
        ]
        
        # Ping interval (10 minutes to stay well under 15-minute timeout)
        self.ping_interval = 600  # 10 minutes in seconds
        
        # Statistics tracking
        self.stats = {
            "total_pings": 0,
            "successful_pings": 0,
            "failed_pings": 0,
            "cold_starts_prevented": 0,
            "last_ping_time": None
        }
    
    async def ping_service(self, service: Dict[str, Any]) -> Dict[str, Any]:
        """Ping a single service and return status."""
        start_time = datetime.now()
        
        try:
            timeout = aiohttp.ClientTimeout(total=service["timeout"])
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                url = f"{service['url']}{service['health_path']}"
                
                async with session.get(url) as response:
                    response_time = (datetime.now() - start_time).total_seconds()
                    
                    # Determine if this was likely a cold start
                    cold_start = response_time > 5.0  # >5 seconds likely indicates cold start
                    
                    result = {
                        "service": service["name"],
                        "status": "success" if response.status < 400 else "error",
                        "status_code": response.status,
                        "response_time": response_time,
                        "cold_start": cold_start,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    if cold_start:
                        logger.warning(f"🟡 {service['name']}: Cold start detected ({response_time:.1f}s)")
                    else:
                        logger.info(f"✅ {service['name']}: Healthy ({response_time:.1f}s)")
                    
                    return result
                    
        except asyncio.TimeoutError:
            result = {
                "service": service["name"],
                "status": "timeout",
                "status_code": None,
                "response_time": service["timeout"],
                "cold_start": True,
                "timestamp": datetime.now().isoformat(),
                "error": "Request timeout"
            }
            logger.error(f"❌ {service['name']}: Timeout after {service['timeout']}s")
            return result
            
        except Exception as e:
            result = {
                "service": service["name"],
                "status": "error",
                "status_code": None,
                "response_time": (datetime.now() - start_time).total_seconds(),
                "cold_start": False,
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
            logger.error(f"❌ {service['name']}: Error - {str(e)}")
            return result
    
    async def ping_all_services(self) -> List[Dict[str, Any]]:
        """Ping all services concurrently."""
        logger.info(f"🔄 Pinging {len(self.services)} services...")
        
        # Ping all services concurrently
        tasks = [self.ping_service(service) for service in self.services]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results and update statistics
        successful = 0
        failed = 0
        cold_starts = 0
        
        for result in results:
            if isinstance(result, dict):
                if result["status"] == "success":
                    successful += 1
                else:
                    failed += 1
                
                if result.get("cold_start"):
                    cold_starts += 1
            else:
                failed += 1
                logger.error(f"Unexpected result: {result}")
        
        # Update statistics
        self.stats["total_pings"] += len(self.services)
        self.stats["successful_pings"] += successful
        self.stats["failed_pings"] += failed
        self.stats["cold_starts_prevented"] += cold_starts
        self.stats["last_ping_time"] = datetime.now().isoformat()
        
        logger.info(f"📊 Ping complete: {successful} successful, {failed} failed, {cold_starts} cold starts")
        
        return results
    
    async def run_keep_alive_loop(self):
        """Main keep-alive loop that runs continuously."""
        logger.info(f"🚀 Starting Keep-Alive Service")
        logger.info(f"📅 Ping interval: {self.ping_interval} seconds ({self.ping_interval/60:.1f} minutes)")
        logger.info(f"🎯 Services to monitor: {len(self.services)}")
        
        while True:
            try:
                # Ping all services
                await self.ping_all_services()
                
                # Log current statistics
                logger.info(f"📈 Total pings: {self.stats['total_pings']}, "
                          f"Success rate: {(self.stats['successful_pings']/max(self.stats['total_pings'], 1)*100):.1f}%")
                
                # Wait for next ping cycle
                logger.info(f"⏰ Next ping in {self.ping_interval/60:.1f} minutes...")
                await asyncio.sleep(self.ping_interval)
                
            except Exception as e:
                logger.error(f"💥 Keep-alive loop error: {e}")
                # Wait 1 minute before retrying on error
                await asyncio.sleep(60)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics."""
        return {
            **self.stats,
            "ping_interval_minutes": self.ping_interval / 60,
            "services_monitored": len(self.services),
            "uptime_percentage": (self.stats["successful_pings"] / max(self.stats["total_pings"], 1)) * 100
        }

# Health endpoint for the keep-alive service itself
from flask import Flask, jsonify

app = Flask(__name__)
keep_alive = KeepAliveService()

@app.route('/health')
def health():
    """Health check endpoint for the keep-alive service."""
    return jsonify({
        "service": "Keep-Alive Service",
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "stats": keep_alive.get_stats()
    })

@app.route('/stats')
def stats():
    """Get detailed statistics."""
    return jsonify(keep_alive.get_stats())

async def run_keep_alive():
    """Run the keep-alive service."""
    await keep_alive.run_keep_alive_loop()

if __name__ == "__main__":
    # Run keep-alive service
    asyncio.run(run_keep_alive())