package com.kclgroup.backend.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.kclgroup.backend.pojo.entity.FinancialData;
import com.kclgroup.backend.pojo.vo.FinancialDataVo;
import com.kclgroup.backend.pojo.vo.FinancialYearData;
import com.kclgroup.backend.service.FinancialDataService;
import com.kclgroup.backend.mapper.FinancialDataMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
* @author 张小明
* @description 针对表【financial_data】的数据库操作Service实现
* @createDate 2024-06-25 16:35:57
*/
@Service
public class FinancialDataServiceImpl extends ServiceImpl<FinancialDataMapper, FinancialData>
    implements FinancialDataService{
    @Autowired
    FinancialDataMapper financialDataMapper;
    @Override
    public FinancialData getByStockCode(String stockCode) {
        FinancialData financialData = baseMapper.getByStockCode(stockCode);
        return financialData;
    }

    @Override
    public FinancialDataVo getFinancialDataByStockCode(String stockCode) {
        List<FinancialData> dataList = financialDataMapper.findByStockCode(stockCode);
        if (dataList.isEmpty()) {
            return null;
        }

        FinancialDataVo vo = new FinancialDataVo(stockCode, dataList.get(0).getSummary()); // Assuming all summaries are the same
        dataList.forEach(data -> {
            FinancialYearData yearData = new FinancialYearData(data.getTotalOperatereveIncrease(), data.getParentNetprofitIncrease(), data.getDnetprofitatpcTcalIncrease());
            vo.addFinancialYearData(data.getYear(), yearData);
        });

        return vo;
    }

}




