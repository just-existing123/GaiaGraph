// File: Company.cpp
#include "Company.h"

Company::Company(ID id, const std::string& name, const std::string& sector, double baseScore)
    : id(id), name(name), sector(sector), baseGreenScore(baseScore), adjustedGreenScore(baseScore) {}

Company::ID Company::getID() const { return id; }
const std::string& Company::getName() const { return name; }
const std::string& Company::getSector() const { return sector; }
double Company::getBaseGreenScore() const { return baseGreenScore; }
double Company::getAdjustedGreenScore() const { return adjustedGreenScore; }
void Company::setBaseGreenScore(double score) { baseGreenScore = score; }
void Company::setAdjustedGreenScore(double score) { adjustedGreenScore = score; }


